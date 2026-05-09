import type { DomainRoute } from '@interceptor/browser/handler/domain-loader';
import { db, fighters, oddsSnapshots, sql, unmatchedOdds } from '@interceptor/db';
import { DEBUG, rateLimitedFetch } from '@interceptor/shared';
import { cacheControlHeader, cacheGet, cacheSet } from './cache';

type RouteCtx = {
	req: { url: string };
	header: (k: string, v: string) => void;
	json: (body: unknown, status?: number) => Response;
};

const ODDS_API_BASE_URL = 'https://api.the-odds-api.com/v4';
const MMA_SPORT_KEY = 'mma_mixed_martial_arts';
const UPCOMING_CACHE_KEY = 'mma_mixed_martial_arts-us-h2h';

type OddsOutcome = {
	name: string;
	price: number;
};

type OddsMarket = {
	key: string;
	outcomes: OddsOutcome[];
};

type OddsBookmaker = {
	key: string;
	title: string;
	markets: OddsMarket[];
};

type OddsEvent = {
	id: string;
	sport_key: string;
	sport_title: string;
	commence_time: string;
	home_team: string;
	away_team: string;
	bookmakers: OddsBookmaker[];
};

type CanonicalFight = {
	event_id: string;
	event_date: string;
	fight_id: string;
	fighters: Array<{ id: string; name: string }>;
};

type MatchedFight = {
	eventId: string;
	fightId: string;
	fighters: Array<{ id: string; name: string; normalizedName: string }>;
};

function parseJsonOrText(text: string): unknown {
	try {
		return JSON.parse(text) as unknown;
	} catch {
		return { error: text };
	}
}

function isOddsEventList(body: unknown): body is OddsEvent[] {
	if (!Array.isArray(body)) return false;
	return body.every((event) => {
		if (!event || typeof event !== 'object') return false;
		const candidate = event as Partial<OddsEvent>;
		return (
			typeof candidate.id === 'string' &&
			Array.isArray(candidate.bookmakers) &&
			candidate.bookmakers.every(
				(bookmaker) =>
					bookmaker &&
					typeof bookmaker === 'object' &&
					typeof (bookmaker as Partial<OddsBookmaker>).key === 'string' &&
					Array.isArray((bookmaker as Partial<OddsBookmaker>).markets),
			)
		);
	});
}

function oddsNameToFighterId(name: string): string {
	const slug = name
		.toLowerCase()
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-+|-+$/g, '');
	if (!slug) {
		throw new Error('Cannot derive fighter id from an empty odds outcome name');
	}
	return `odds:${slug}`;
}

function normalizeName(name: string): string {
	return name.toLowerCase().replace(/[^a-z0-9]+/g, '');
}

function pairKey(date: string, fighterA: string, fighterB: string): string {
	const names = [normalizeName(fighterA), normalizeName(fighterB)].sort();
	return `${date}:${names[0]}:${names[1]}`;
}

function eventDateFromCommenceTime(commenceTime: string): string | null {
	const date = new Date(commenceTime);
	if (Number.isNaN(date.getTime())) return null;
	return date.toISOString().slice(0, 10);
}

function decimalToAmerican(decimalOdds: number): number {
	if (decimalOdds < 1) {
		throw new Error(`Invalid decimal odds ${decimalOdds}`);
	}
	if (decimalOdds === 1) return -100_000;
	if (decimalOdds >= 2) {
		return Math.round((decimalOdds - 1) * 100);
	}
	return Math.round(-100 / (decimalOdds - 1));
}

async function fetchUpcomingOdds(): Promise<{
	body: unknown;
	status: number;
	requestsRemaining: string | null;
}> {
	const apiKey = process.env.ODDS_API_KEY;
	if (!apiKey) {
		return {
			body: { error: 'ODDS_API_KEY is required for /api/odds-mma/upcoming' },
			status: 500,
			requestsRemaining: null,
		};
	}

	const url = new URL(`${ODDS_API_BASE_URL}/sports/${MMA_SPORT_KEY}/odds`);
	url.searchParams.set('regions', 'us');
	url.searchParams.set('markets', 'h2h');
	url.searchParams.set('apiKey', apiKey);

	const res = await rateLimitedFetch(url, {
		headers: { Accept: 'application/json' },
	});
	const requestsRemaining = res.headers.get('x-requests-remaining');
	if (requestsRemaining) {
		DEBUG('odds-mma', `x-requests-remaining=${requestsRemaining}`);
	}

	const body = parseJsonOrText(await res.text());
	return {
		body,
		status: res.ok ? 200 : res.status,
		requestsRemaining,
	};
}

async function cachedUpcoming(c: RouteCtx): Promise<Response> {
	const url = new URL(c.req.url);
	const bypass = url.searchParams.get('refresh') === '1' || url.searchParams.get('nocache') === '1';

	if (!bypass) {
		const hit = cacheGet<unknown>('oddsList', UPCOMING_CACHE_KEY);
		if (hit) {
			c.header('X-Cache', 'HIT');
			c.header('Cache-Control', cacheControlHeader('oddsList'));
			return c.json(hit);
		}
	}

	const result = await fetchUpcomingOdds();
	if (result.requestsRemaining) {
		c.header('X-Odds-Requests-Remaining', result.requestsRemaining);
	}

	if (result.status >= 200 && result.status < 300) {
		cacheSet('oddsList', UPCOMING_CACHE_KEY, result.body);
		c.header('X-Cache', bypass ? 'BYPASS' : 'MISS');
		c.header('Cache-Control', cacheControlHeader('oddsList'));
		return c.json(result.body);
	}

	c.header('X-Cache', 'SKIP');
	return c.json(result.body, result.status);
}

async function loadFightMatchIndex(): Promise<Map<string, MatchedFight>> {
	const rows = await sql<CanonicalFight[]>`
		SELECT
			e.id AS event_id,
			e.date::text AS event_date,
			f.id AS fight_id,
			json_agg(json_build_object('id', fi.id, 'name', fi.name) ORDER BY fi.name) AS fighters
		FROM events e
		JOIN fights f ON f.event_id = e.id
		JOIN fight_results fr ON fr.fight_id = f.id
		JOIN fighters fi ON fi.id = fr.fighter_id
		GROUP BY e.id, e.date, f.id
		HAVING count(*) = 2
	`;
	const index = new Map<string, MatchedFight>();
	for (const row of rows) {
		const [fighterA, fighterB] = row.fighters;
		if (!fighterA || !fighterB) continue;
		index.set(pairKey(row.event_date, fighterA.name, fighterB.name), {
			eventId: row.event_id,
			fightId: row.fight_id,
			fighters: row.fighters.map((fighter) => ({
				...fighter,
				normalizedName: normalizeName(fighter.name),
			})),
		});
	}
	return index;
}

async function snapshotOdds(c: RouteCtx): Promise<Response> {
	const snapshotAt = new Date();
	const snapshotId = snapshotAt.toISOString();
	const result = await fetchUpcomingOdds();
	if (result.requestsRemaining) {
		c.header('X-Odds-Requests-Remaining', result.requestsRemaining);
	}

	if (result.status < 200 || result.status >= 300) {
		return c.json(result.body, result.status);
	}

	if (!isOddsEventList(result.body)) {
		return c.json({ error: 'Unexpected odds API response shape' }, 502);
	}

	const fightIndex = await loadFightMatchIndex();
	const fighterRows = new Map<string, { id: string; name: string }>();
	const oddsRows: (typeof oddsSnapshots.$inferInsert)[] = [];
	const unmatchedRows = new Map<string, typeof unmatchedOdds.$inferInsert>();
	let matchedRows = 0;

	for (const event of result.body) {
		const eventDate = eventDateFromCommenceTime(event.commence_time);
		const matchedFight = eventDate
			? (fightIndex.get(pairKey(eventDate, event.home_team, event.away_team)) ?? null)
			: null;
		if (!matchedFight && eventDate) {
			const unmatchedId = `${snapshotId}:${event.id}`;
			unmatchedRows.set(unmatchedId, {
				id: unmatchedId,
				rawEventName: `${event.away_team} vs ${event.home_team}`,
				rawFighterA: event.away_team,
				rawFighterB: event.home_team,
				rawDate: eventDate,
				snapshotId,
				reason: 'no canonical fight for date and fighter pair',
			});
		}

		for (const bookmaker of event.bookmakers) {
			for (const market of bookmaker.markets) {
				if (market.key !== 'h2h') continue;
				for (const outcome of market.outcomes) {
					if (typeof outcome.name !== 'string' || typeof outcome.price !== 'number') continue;
					const matchedFighter = matchedFight?.fighters.find(
						(fighter) => fighter.normalizedName === normalizeName(outcome.name),
					);
					const fighterId = matchedFighter?.id ?? oddsNameToFighterId(outcome.name);
					if (!matchedFighter) {
						fighterRows.set(fighterId, { id: fighterId, name: outcome.name });
					} else {
						matchedRows++;
					}
					oddsRows.push({
						eventId: matchedFight?.eventId ?? null,
						fightId: matchedFight?.fightId ?? null,
						fighterId,
						snapshotAt,
						bookmaker: bookmaker.key,
						decimalOdds: outcome.price,
						americanOdds: decimalToAmerican(outcome.price),
					});
				}
			}
		}
	}

	const unmatchedValues = Array.from(unmatchedRows.values());
	if (unmatchedValues.length) {
		await db.insert(unmatchedOdds).values(unmatchedValues).onConflictDoNothing();
	}

	if (!oddsRows.length) {
		DEBUG('odds-mma', 'matched 0 of 0 odds rows; 0 unmatched logged');
		return c.json({
			snapshot_id: snapshotId,
			rows_written: 0,
			matched_rows: 0,
			unmatched_logged: unmatchedValues.length,
			requests_remaining: result.requestsRemaining,
		});
	}

	await db.insert(fighters).values(Array.from(fighterRows.values())).onConflictDoNothing();

	const inserted = await db
		.insert(oddsSnapshots)
		.values(oddsRows)
		.onConflictDoNothing()
		.returning({ fighterId: oddsSnapshots.fighterId });

	DEBUG(
		'odds-mma',
		`matched ${matchedRows} of ${oddsRows.length} odds rows; ${unmatchedValues.length} unmatched logged`,
	);

	return c.json({
		snapshot_id: snapshotId,
		rows_written: inserted.length,
		matched_rows: matchedRows,
		unmatched_logged: unmatchedValues.length,
		requests_remaining: result.requestsRemaining,
	});
}

export const routes: DomainRoute[] = [
	{
		method: 'GET',
		path: '/upcoming',
		description: 'Current UFC/MMA moneyline odds from the-odds-api.',
		browserRequired: false,
		handler: cachedUpcoming,
	},
	{
		method: 'GET',
		path: '/snapshot',
		description: 'Persist current UFC/MMA moneyline odds into odds_snapshots.',
		browserRequired: false,
		handler: snapshotOdds,
	},
];
