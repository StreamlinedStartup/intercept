import { createHash } from 'node:crypto';
import { db, sql } from './client.js';
import {
	historicalMoneylineOdds,
	historicalOddsEvents,
	historicalOddsFights,
	historicalOddsImportRuns,
	unmatchedHistoricalOdds,
} from './schema.js';

const SOURCE = 'fightodds';
const GRAPHQL_URL = 'https://api.fightodds.io/gql';
const DEFAULT_EVENT_PK = 5362;
const DEFAULT_FROM = '2024-02-01';
const DEFAULT_TO = '2024-03-10';
const DEFAULT_LIMIT = 3;
const DEFAULT_DELAY_MS = 750;
const DEFAULT_EVENT: EventIndexNode = {
	id: 'RXZlbnROb2RlOjUzNjI=',
	name: 'UFC Fight Night 237: Moreno vs. Royval 2',
	pk: DEFAULT_EVENT_PK,
	slug: 'ufc-fight-night-237-moreno-vs-royval-2',
	date: '2024-02-24',
	venue: 'Arena CDMX',
	city: 'Mexico City, Mexico',
	promotion: {
		slug: 'ufc',
		shortName: 'UFC',
	},
};

type GraphqlResponse<T> = {
	data?: T;
	errors?: unknown;
};

type EventsRecentData = {
	allEvents?: {
		edges: Array<{ cursor: string; node: EventIndexNode }>;
		pageInfo: {
			hasNextPage: boolean;
			endCursor: string | null;
		};
	} | null;
};

type EventOddsData = {
	eventOfferTable?: EventOfferTable | null;
};

type EventIndexNode = {
	id: string;
	name: string;
	pk: number;
	slug: string;
	date: string;
	venue: string | null;
	city: string | null;
	promotion: {
		id?: string;
		slug?: string;
		shortName?: string;
	} | null;
};

type EventOfferTable = {
	id: string;
	pk: number;
	slug: string;
	fightOffers: {
		edges: Array<{ node: FightOfferNode }>;
	};
};

type FightOfferNode = {
	id: string;
	slug: string;
	isCancelled: boolean;
	propCount: number;
	bestOdds1: number | null;
	bestOdds2: number | null;
	fighter1: SourceFighter;
	fighter2: SourceFighter;
	straightOffers: {
		edges: Array<{ node: StraightOfferNode }>;
	};
};

type SourceFighter = {
	id: string;
	firstName: string;
	lastName: string;
	slug: string;
};

type StraightOfferNode = {
	id: string;
	sportsbook: {
		id: string;
		shortName: string;
		slug: string;
	};
	outcome1: SourceOutcome | null;
	outcome2: SourceOutcome | null;
};

type SourceOutcome = {
	id: string;
	odds: number | null;
	oddsPrev: number | null;
};

type MoneylineRow = typeof historicalMoneylineOdds.$inferInsert;

type EventImportSummary = {
	source: typeof SOURCE;
	sourceEventId: string;
	sourceUrl: string;
	eventsRead: number;
	fightsRead: number;
	moneylinesRead: number;
	rowsUpserted: number;
	matchedRows: number;
	unmatchedRows: number;
	skippedRows: number;
	cancelledFights: number;
};

type RangeImportSummary = {
	source: typeof SOURCE;
	from: string;
	to: string;
	limit: number;
	delayMs: number;
	eventsScanned: number;
	eventsImported: number;
	eventsSkipped: number;
	fightsRead: number;
	moneylinesRead: number;
	matchedRows: number;
	unmatchedRows: number;
	skippedRows: number;
	cancelledFights: number;
	sourceEventIds: string[];
};

type ImportOptions = {
	from: string;
	to: string;
	limit: number;
	delayMs: number;
};

function usage() {
	console.log(`Usage:
  pnpm --filter @interceptor/db import:fightodds:event
  pnpm --filter @interceptor/db import:fightodds:range -- --from 2024-02-01 --to 2024-03-10 --limit 3

The range importer uses FightOdds allEvents pagination, filters to UFC events, and imports each event's moneyline odds with deterministic ids.`);
}

async function main() {
	if (process.argv.includes('--help') || process.argv.includes('-h')) {
		usage();
		process.exit(0);
	}

	const options = parseArgs(process.argv.slice(2));
	const isRangeCommand = process.env.FIGHTODDS_RANGE_IMPORT === '1' || hasRangeArg(process.argv);
	const summary = isRangeCommand
		? await importFightOddsRange(options)
		: await importFightOddsEvent(DEFAULT_EVENT_PK);
	console.log(JSON.stringify(summary, null, 2));
}

export async function importFightOddsEvent(
	eventPk = DEFAULT_EVENT_PK,
): Promise<EventImportSummary> {
	const event = eventPk === DEFAULT_EVENT_PK ? DEFAULT_EVENT : await fetchEventIndexByPk(eventPk);
	if (!event) {
		throw new Error(`No FightOdds event found for pk=${eventPk}`);
	}
	return importFightOddsEventNode(event);
}

export async function importFightOddsRange(options: ImportOptions): Promise<RangeImportSummary> {
	const events = await fetchEventIndexRange(options);
	const imported: EventImportSummary[] = [];
	let eventsSkipped = 0;
	for (const [index, event] of events.entries()) {
		if (!isUfcEvent(event)) {
			eventsSkipped += 1;
			continue;
		}
		if (imported.length >= options.limit) {
			eventsSkipped += 1;
			continue;
		}
		imported.push(await importFightOddsEventNode(event));
		if (index < events.length - 1 && options.delayMs > 0) {
			await sleep(options.delayMs);
		}
	}
	return {
		source: SOURCE,
		from: options.from,
		to: options.to,
		limit: options.limit,
		delayMs: options.delayMs,
		eventsScanned: events.length,
		eventsImported: imported.length,
		eventsSkipped,
		fightsRead: sum(imported, 'fightsRead'),
		moneylinesRead: sum(imported, 'moneylinesRead'),
		matchedRows: sum(imported, 'matchedRows'),
		unmatchedRows: sum(imported, 'unmatchedRows'),
		skippedRows: sum(imported, 'skippedRows'),
		cancelledFights: sum(imported, 'cancelledFights'),
		sourceEventIds: imported.map((event) => event.sourceEventId),
	};
}

async function importFightOddsEventNode(event: EventIndexNode): Promise<EventImportSummary> {
	const startedAt = new Date();
	const scrapedAt = startedAt;
	const sourceEventId = String(event.pk);
	const eventOfferTable = await fetchEventOfferTable(event.pk);
	if (eventOfferTable.pk !== event.pk) {
		throw new Error(`Expected FightOdds event ${event.pk}; received ${eventOfferTable.pk}`);
	}

	const historicalEventId = eventId(sourceEventId);
	const fights = eventOfferTable.fightOffers.edges.map((edge) => edge.node);
	const { rows: moneylineRows, skippedRows } = buildMoneylineRows(sourceEventId, fights, scrapedAt);
	const unmatchedRows = fights.map((fight) => ({
		id: stableId(SOURCE, 'unmatched', sourceEventId, fight.id),
		source: SOURCE,
		sourceEventId,
		sourceFightId: fight.id,
		sourceUrl: fightUrl(fight.slug),
		rawEventName: event.name,
		rawEventDate: dateOnly(event.date),
		rawFighterA: fighterName(fight.fighter1),
		rawFighterB: fighterName(fight.fighter2),
		rawSportsbook: null,
		rawOdds: stringifyJson({
			bestOdds1: fight.bestOdds1,
			bestOdds2: fight.bestOdds2,
			straightOfferCount: fight.straightOffers.edges.length,
		}),
		candidateMatches: stringifyJson([]),
		reason: 'canonical matching pending',
		reviewed: false,
		reviewedAt: null,
		reviewNote: null,
	}));
	const finishedAt = new Date();
	const matchedRows = 0;
	const unmatchedRowCount = fights.length;
	const importRunId = importRunIdFor(sourceEventId);
	const sourceUrl = eventUrl(event.pk, event.slug);

	await db.transaction(async (tx) => {
		await tx
			.insert(historicalOddsImportRuns)
			.values({
				id: importRunId,
				source: SOURCE,
				sourceUrl,
				sourceEventId,
				startedAt,
				finishedAt,
				status: 'completed',
				eventsRead: 1,
				fightsRead: fights.length,
				moneylinesRead: moneylineRows.length,
				matchedRows,
				unmatchedRows: unmatchedRowCount,
				rawMetadata: stringifyJson({
					operationName: 'EventOddsQuery',
					variables: { eventPk: event.pk },
					sourceEventGlobalId: event.id,
				}),
			})
			.onConflictDoUpdate({
				target: historicalOddsImportRuns.id,
				set: {
					startedAt,
					finishedAt,
					status: 'completed',
					eventsRead: 1,
					fightsRead: fights.length,
					moneylinesRead: moneylineRows.length,
					matchedRows,
					unmatchedRows: unmatchedRowCount,
					rawMetadata: stringifyJson({
						operationName: 'EventOddsQuery',
						variables: { eventPk: event.pk },
						sourceEventGlobalId: event.id,
					}),
				},
			});

		await tx
			.insert(historicalOddsEvents)
			.values({
				id: historicalEventId,
				source: SOURCE,
				sourceEventId,
				sourceEventGlobalId: eventOfferTable.id,
				sourceSlug: eventOfferTable.slug,
				sourceUrl,
				rawName: event.name,
				eventDate: dateOnly(event.date),
				venue: event.venue,
				city: event.city,
				promotion: event.promotion?.shortName ?? 'unknown',
				canonicalEventId: null,
				matchStatus: 'unmatched',
				matchReason: 'canonical matching pending',
				rawMetadata: stringifyJson({
					pk: eventOfferTable.pk,
					id: eventOfferTable.id,
					slug: eventOfferTable.slug,
					index: event,
				}),
				scrapedAt,
				updatedAt: finishedAt,
			})
			.onConflictDoUpdate({
				target: historicalOddsEvents.id,
				set: {
					sourceEventGlobalId: eventOfferTable.id,
					sourceSlug: eventOfferTable.slug,
					sourceUrl,
					rawName: event.name,
					eventDate: dateOnly(event.date),
					venue: event.venue,
					city: event.city,
					promotion: event.promotion?.shortName ?? 'unknown',
					rawMetadata: stringifyJson({
						pk: eventOfferTable.pk,
						id: eventOfferTable.id,
						slug: eventOfferTable.slug,
						index: event,
					}),
					scrapedAt,
					updatedAt: finishedAt,
				},
			});

		for (const fight of fights) {
			await tx
				.insert(historicalOddsFights)
				.values({
					id: fightId(sourceEventId, fight.id),
					historicalEventId,
					sourceFightId: fight.id,
					sourceFightSlug: fight.slug,
					sourceUrl: fightUrl(fight.slug),
					rawFighterA: fighterName(fight.fighter1),
					rawFighterB: fighterName(fight.fighter2),
					sourceFighterAId: fight.fighter1.id,
					sourceFighterBId: fight.fighter2.id,
					sourceFighterASlug: fight.fighter1.slug,
					sourceFighterBSlug: fight.fighter2.slug,
					isCancelled: fight.isCancelled,
					propCount: fight.propCount,
					bestOddsA: fight.bestOdds1,
					bestOddsB: fight.bestOdds2,
					canonicalFightId: null,
					canonicalFighterAId: null,
					canonicalFighterBId: null,
					matchStatus: 'unmatched',
					matchReason: 'canonical matching pending',
					candidateMatches: stringifyJson([]),
					rawMetadata: stringifyJson({
						id: fight.id,
						slug: fight.slug,
						isCancelled: fight.isCancelled,
						propCount: fight.propCount,
						bestOdds1: fight.bestOdds1,
						bestOdds2: fight.bestOdds2,
					}),
					scrapedAt,
					updatedAt: finishedAt,
				})
				.onConflictDoUpdate({
					target: historicalOddsFights.id,
					set: {
						sourceFightSlug: fight.slug,
						sourceUrl: fightUrl(fight.slug),
						rawFighterA: fighterName(fight.fighter1),
						rawFighterB: fighterName(fight.fighter2),
						sourceFighterAId: fight.fighter1.id,
						sourceFighterBId: fight.fighter2.id,
						sourceFighterASlug: fight.fighter1.slug,
						sourceFighterBSlug: fight.fighter2.slug,
						isCancelled: fight.isCancelled,
						propCount: fight.propCount,
						bestOddsA: fight.bestOdds1,
						bestOddsB: fight.bestOdds2,
						rawMetadata: stringifyJson({
							id: fight.id,
							slug: fight.slug,
							isCancelled: fight.isCancelled,
							propCount: fight.propCount,
							bestOdds1: fight.bestOdds1,
							bestOdds2: fight.bestOdds2,
						}),
						scrapedAt,
						updatedAt: finishedAt,
					},
				});
		}

		for (const row of moneylineRows) {
			await tx
				.insert(historicalMoneylineOdds)
				.values(row)
				.onConflictDoUpdate({
					target: historicalMoneylineOdds.id,
					set: {
						americanOdds: row.americanOdds,
						decimalOdds: row.decimalOdds,
						impliedProbability: row.impliedProbability,
						marketTimestamp: row.marketTimestamp,
						marketTimestampSemantics: row.marketTimestampSemantics,
						scrapedAt,
						rawMetadata: row.rawMetadata,
						updatedAt: finishedAt,
					},
				});
		}

		for (const row of unmatchedRows) {
			await tx.insert(unmatchedHistoricalOdds).values(row).onConflictDoNothing();
		}
	});

	return {
		source: SOURCE,
		sourceEventId,
		sourceUrl,
		eventsRead: 1,
		fightsRead: fights.length,
		moneylinesRead: moneylineRows.length,
		rowsUpserted: 1 + fights.length + moneylineRows.length + unmatchedRows.length,
		matchedRows,
		unmatchedRows: unmatchedRowCount,
		skippedRows,
		cancelledFights: fights.filter((fight) => fight.isCancelled).length,
	};
}

async function fetchEventIndexRange(options: ImportOptions): Promise<EventIndexNode[]> {
	const events: EventIndexNode[] = [];
	let cursor: string | null = null;
	while (events.filter(isUfcEvent).length < options.limit) {
		const page: EventsRecentData = await graphql<EventsRecentData>({
			operationName: 'EventsRecentQuery',
			variables: {
				after: cursor,
				first: 10,
				dateGte: options.from,
				dateLt: options.to,
				orderBy: '-date',
			},
			query: EVENTS_RECENT_QUERY,
		});
		const connection: NonNullable<EventsRecentData['allEvents']> | null | undefined =
			page.allEvents;
		if (!connection) {
			throw new Error('FightOdds EventsRecentQuery returned no allEvents connection');
		}
		events.push(
			...connection.edges.map((edge: { cursor: string; node: EventIndexNode }) => edge.node),
		);
		if (!connection.pageInfo.hasNextPage || !connection.pageInfo.endCursor) {
			break;
		}
		cursor = connection.pageInfo.endCursor;
	}
	return events;
}

async function fetchEventIndexByPk(eventPk: number): Promise<EventIndexNode | null> {
	const to = new Date();
	to.setUTCFullYear(to.getUTCFullYear() + 1);
	const events = await fetchEventIndexRange({
		from: '1993-01-01',
		to: to.toISOString().slice(0, 10),
		limit: 2000,
		delayMs: 0,
	});
	return events.find((event) => event.pk === eventPk) ?? null;
}

async function fetchEventOfferTable(eventPk: number): Promise<EventOfferTable> {
	const body = await graphql<EventOddsData>({
		operationName: 'EventOddsQuery',
		variables: { eventPk },
		query: EVENT_ODDS_QUERY,
	});
	const eventOfferTable = body.eventOfferTable;
	if (!eventOfferTable) {
		throw new Error(`FightOdds EventOddsQuery returned no eventOfferTable for pk=${eventPk}`);
	}
	return eventOfferTable;
}

async function graphql<T>(payload: {
	operationName: string;
	variables: Record<string, unknown>;
	query: string;
}): Promise<T> {
	const response = await fetch(GRAPHQL_URL, {
		method: 'POST',
		headers: { 'content-type': 'application/json' },
		body: JSON.stringify(payload),
	});

	if (!response.ok) {
		throw new Error(`FightOdds ${payload.operationName} failed with HTTP ${response.status}`);
	}

	const body = (await response.json()) as GraphqlResponse<T>;
	if (body.errors) {
		throw new Error(
			`FightOdds ${payload.operationName} returned errors: ${stringifyJson(body.errors)}`,
		);
	}
	if (!body.data) {
		throw new Error(`FightOdds ${payload.operationName} returned no data`);
	}
	return body.data;
}

function buildMoneylineRows(
	sourceEventId: string,
	fights: FightOfferNode[],
	scrapedAt: Date,
): { rows: MoneylineRow[]; skippedRows: number } {
	const rows: MoneylineRow[] = [];
	let skippedRows = 0;
	for (const fight of fights) {
		for (const edge of fight.straightOffers.edges) {
			const offer = edge.node;
			const outcome1 = outcomeRows({
				sourceEventId,
				historicalFightId: fightId(sourceEventId, fight.id),
				offer,
				fighter: fight.fighter1,
				rawFighterName: fighterName(fight.fighter1),
				side: 'fighter_a',
				outcome: offer.outcome1,
				scrapedAt,
			});
			const outcome2 = outcomeRows({
				sourceEventId,
				historicalFightId: fightId(sourceEventId, fight.id),
				offer,
				fighter: fight.fighter2,
				rawFighterName: fighterName(fight.fighter2),
				side: 'fighter_b',
				outcome: offer.outcome2,
				scrapedAt,
			});
			rows.push(...outcome1.rows, ...outcome2.rows);
			skippedRows += outcome1.skippedRows + outcome2.skippedRows;
		}
	}
	return { rows, skippedRows };
}

function outcomeRows(input: {
	sourceEventId: string;
	historicalFightId: string;
	offer: StraightOfferNode;
	fighter: SourceFighter;
	rawFighterName: string;
	side: 'fighter_a' | 'fighter_b';
	outcome: SourceOutcome | null;
	scrapedAt: Date;
}): { rows: MoneylineRow[]; skippedRows: number } {
	const rows: MoneylineRow[] = [];
	let skippedRows = 0;
	if (input.outcome === null) {
		return { rows, skippedRows: 2 };
	}
	const rowInput = { ...input, outcome: input.outcome };
	if (input.outcome.odds !== null) {
		rows.push(moneylineRow(rowInput, input.outcome.odds, 'source_current'));
	} else {
		skippedRows += 1;
	}
	if (input.outcome.oddsPrev !== null) {
		rows.push(moneylineRow(rowInput, input.outcome.oddsPrev, 'source_previous'));
	} else {
		skippedRows += 1;
	}
	return { rows, skippedRows };
}

function moneylineRow(
	input: {
		sourceEventId: string;
		historicalFightId: string;
		offer: StraightOfferNode;
		fighter: SourceFighter;
		rawFighterName: string;
		side: 'fighter_a' | 'fighter_b';
		outcome: SourceOutcome;
		scrapedAt: Date;
	},
	americanOdds: number,
	lineKind: 'source_current' | 'source_previous',
): MoneylineRow {
	const importRunId = importRunIdFor(input.sourceEventId);
	return {
		id: stableId(SOURCE, 'moneyline', importRunId, input.offer.id, input.outcome.id, lineKind),
		importRunId,
		historicalFightId: input.historicalFightId,
		sourceOfferId: input.offer.id,
		sportsbookId: input.offer.sportsbook.id,
		sportsbookSlug: input.offer.sportsbook.slug,
		sportsbookName: input.offer.sportsbook.shortName,
		sourceOutcomeId: input.outcome.id,
		rawFighterName: input.rawFighterName,
		sourceFighterId: input.fighter.id,
		canonicalFighterId: null,
		side: input.side,
		lineKind,
		americanOdds,
		decimalOdds: americanToDecimal(americanOdds),
		impliedProbability: americanToImpliedProbability(americanOdds),
		marketTimestamp: null,
		marketTimestampSemantics:
			lineKind === 'source_current' ? 'source_current_at_scrape' : 'source_previous_unknown_time',
		scrapedAt: input.scrapedAt,
		rawMetadata: stringifyJson({
			offerId: input.offer.id,
			outcomeId: input.outcome.id,
			lineKind,
			odds: americanOdds,
			sportsbook: input.offer.sportsbook,
		}),
	};
}

export function americanToDecimal(americanOdds: number): number {
	if (americanOdds === 0) {
		throw new Error('American odds cannot be zero');
	}
	return americanOdds > 0 ? 1 + americanOdds / 100 : 1 + 100 / Math.abs(americanOdds);
}

export function americanToImpliedProbability(americanOdds: number): number {
	if (americanOdds === 0) {
		throw new Error('American odds cannot be zero');
	}
	return americanOdds > 0
		? 100 / (americanOdds + 100)
		: Math.abs(americanOdds) / (Math.abs(americanOdds) + 100);
}

function parseArgs(args: string[]): ImportOptions {
	return {
		from: readArg(args, '--from') ?? DEFAULT_FROM,
		to: readArg(args, '--to') ?? DEFAULT_TO,
		limit: Number(readArg(args, '--limit') ?? DEFAULT_LIMIT),
		delayMs: Number(readArg(args, '--delay-ms') ?? DEFAULT_DELAY_MS),
	};
}

function readArg(args: string[], name: string): string | null {
	const index = args.indexOf(name);
	if (index === -1) {
		return null;
	}
	const value = args[index + 1];
	if (!value || value.startsWith('--')) {
		throw new Error(`${name} requires a value`);
	}
	return value;
}

function hasRangeArg(args: string[]): boolean {
	return ['--from', '--to', '--limit', '--delay-ms'].some((arg) => args.includes(arg));
}

function isUfcEvent(event: EventIndexNode): boolean {
	return event.promotion?.slug === 'ufc' || event.promotion?.shortName === 'UFC';
}

function eventId(sourceEventId: string): string {
	return stableId(SOURCE, 'event', sourceEventId);
}

function fightId(sourceEventId: string, sourceFightId: string): string {
	return stableId(SOURCE, 'fight', sourceEventId, sourceFightId);
}

function importRunIdFor(sourceEventId: string): string {
	return `${SOURCE}:${sourceEventId}:single-event-moneyline`;
}

function eventUrl(pk: number, slug: string): string {
	return `https://fightodds.io/mma-events/${pk}/${slug}/odds`;
}

function fightUrl(slug: string): string {
	return `https://fightodds.io/mma-bouts/${slug}/odds`;
}

function fighterName(fighter: SourceFighter): string {
	return `${fighter.firstName} ${fighter.lastName}`.trim();
}

function dateOnly(value: string): string {
	return value.slice(0, 10);
}

function stableId(...parts: string[]): string {
	return createHash('sha256').update(parts.join('\0')).digest('hex').slice(0, 32);
}

function stringifyJson(value: unknown): string {
	return JSON.stringify(value);
}

function sleep(ms: number): Promise<void> {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

function sum(rows: EventImportSummary[], key: keyof EventImportSummary): number {
	return rows.reduce((total, row) => total + Number(row[key]), 0);
}

const EVENTS_RECENT_QUERY = `query EventsRecentQuery($after: String, $first: Int!, $dateGte: Date, $dateLt: Date, $orderBy: String) {
	allEvents(first: $first, after: $after, date_Gte: $dateGte, date_Lt: $dateLt, orderBy: $orderBy) {
		edges {
			cursor
			node {
				id
				name
				pk
				slug
				date
				venue
				city
				promotion { id slug shortName }
			}
		}
		pageInfo { hasNextPage endCursor }
	}
}`;

const EVENT_ODDS_QUERY = `query EventOddsQuery($eventPk: Int!) {
	eventOfferTable(pk: $eventPk) {
		id
		pk
		slug
		fightOffers {
			edges {
				node {
					id
					slug
					isCancelled
					propCount
					bestOdds1
					bestOdds2
					fighter1 { id firstName lastName slug }
					fighter2 { id firstName lastName slug }
					straightOffers {
						edges {
							node {
								id
								sportsbook { id shortName slug }
								outcome1 { id odds oddsPrev }
								outcome2 { id odds oddsPrev }
							}
						}
					}
				}
			}
		}
	}
}`;

if (process.argv[1]?.endsWith('import-fightodds-event.ts')) {
	main()
		.catch((error) => {
			console.error(error instanceof Error ? error.message : error);
			process.exit(1);
		})
		.finally(async () => {
			await sql.end();
		});
}
