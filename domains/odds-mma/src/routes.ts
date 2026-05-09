import type { DomainRoute } from '@interceptor/browser/handler/domain-loader';
import { db, fighters, oddsSnapshots } from '@interceptor/db';
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

	const fighterRows = new Map<string, { id: string; name: string }>();
	const oddsRows: (typeof oddsSnapshots.$inferInsert)[] = [];

	for (const event of result.body) {
		for (const bookmaker of event.bookmakers) {
			for (const market of bookmaker.markets) {
				if (market.key !== 'h2h') continue;
				for (const outcome of market.outcomes) {
					if (typeof outcome.name !== 'string' || typeof outcome.price !== 'number') continue;
					const fighterId = oddsNameToFighterId(outcome.name);
					fighterRows.set(fighterId, { id: fighterId, name: outcome.name });
					oddsRows.push({
						eventId: null,
						fightId: null,
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

	if (!oddsRows.length) {
		return c.json({
			snapshot_id: snapshotId,
			rows_written: 0,
			requests_remaining: result.requestsRemaining,
		});
	}

	await db.insert(fighters).values(Array.from(fighterRows.values())).onConflictDoNothing();

	const inserted = await db
		.insert(oddsSnapshots)
		.values(oddsRows)
		.onConflictDoNothing()
		.returning({ fighterId: oddsSnapshots.fighterId });

	return c.json({
		snapshot_id: snapshotId,
		rows_written: inserted.length,
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
