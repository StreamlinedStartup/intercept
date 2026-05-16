import { createHash } from 'node:crypto';
import { db, sql } from './client.js';
import {
	historicalMoneylineOdds,
	historicalOddsEvents,
	historicalOddsFights,
	historicalOddsImportRuns,
	historicalPropOdds,
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

type FightPropOffersData = {
	fightPropOfferTable?: FightPropOfferTable | null;
};

type EventHeaderData = {
	event?: EventIndexNode | null;
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
type PropOddsRow = typeof historicalPropOdds.$inferInsert;

type FightPropOfferTable = {
	id: string;
	fight: {
		id: string;
		pk: number;
		slug: string;
		fighter1: SourceFighter;
		fighter2: SourceFighter;
		fightItdOdds: number | null;
		fighter1ItdOdds: number | null;
		fighter2ItdOdds: number | null;
		fighter1KoOdds: number | null;
		fighter2KoOdds: number | null;
		fighter1SubOdds: number | null;
		fighter2SubOdds: number | null;
		fighter1DecOdds: number | null;
		fighter2DecOdds: number | null;
	};
	propOffers: {
		edges: Array<{ node: PropOfferNode }>;
	};
};

type PropOfferNode = {
	offerType: {
		offerTypeId: string;
		category: string;
		subCategory: string;
		description: string;
		value: string | null;
		notDescription: string;
	};
	propName1: string;
	propName2: string;
	bestOdds1: number | null;
	bestOdds2: number | null;
	offers: {
		edges: Array<{ node: PropSportsbookOfferNode }>;
	};
};

type PropSportsbookOfferNode = {
	id: string;
	sportsbook: {
		id: string;
		shortName: string;
		slug: string;
	};
	outcome1: PropOutcome | null;
	outcome2: PropOutcome | null;
};

type PropOutcome = {
	id: string;
	name: string;
	odds: number | null;
	oddsPrev: number | null;
	oddsOpen: number | null;
	oddsBest: number | null;
	oddsWorst: number | null;
	isNot: boolean;
	fighter: SourceFighter | null;
};

type PropImportResult = {
	rows: PropOddsRow[];
	skippedRows: number;
	marketsRead: number;
	marketsImported: number;
	marketsSkipped: number;
	skippedMarketReasons: Record<string, number>;
};

type EventImportSummary = {
	source: typeof SOURCE;
	sourceEventId: string;
	sourceUrl: string;
	eventsRead: number;
	fightsRead: number;
	moneylinesRead: number;
	propLinesRead: number;
	propLinesSkipped: number;
	propMarketsRead: number;
	propMarketsImported: number;
	propMarketsSkipped: number;
	propSkippedMarketReasons: Record<string, number>;
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
	eventsFailed: number;
	fightsRead: number;
	moneylinesRead: number;
	propLinesRead: number;
	propLinesSkipped: number;
	propMarketsRead: number;
	propMarketsImported: number;
	propMarketsSkipped: number;
	propSkippedMarketReasons: Record<string, number>;
	matchedRows: number;
	unmatchedRows: number;
	skippedRows: number;
	cancelledFights: number;
	sourceEventIds: string[];
	failedEvents: Array<{ sourceEventId: string; error: string }>;
};

type ImportOptions = {
	from: string;
	to: string;
	limit: number;
	delayMs: number;
	eventPks: number[];
	continueOnError: boolean;
	includeProps: boolean;
};

type EventImportOptions = {
	includeProps: boolean;
};

function usage() {
	console.log(`Usage:
  pnpm --filter @interceptor/db import:fightodds:event
  pnpm --filter @interceptor/db import:fightodds:event -- --include-props
  pnpm --filter @interceptor/db import:fightodds:event -- --event-pks 5356,5318,5362 --continue-on-error
  pnpm --filter @interceptor/db import:fightodds:range -- --from 2024-02-01 --to 2024-03-10 --limit 3

The range importer uses FightOdds allEvents pagination, filters to UFC events, and imports each event's moneyline odds with deterministic ids.
The explicit event-pk importer uses sitemap/discovered event ids and avoids the allEvents pagination endpoint.
The optional --include-props flag imports the first decision/finish prop slice: the two-way DISTANCE market.`);
}

async function main() {
	if (process.argv.includes('--help') || process.argv.includes('-h')) {
		usage();
		process.exit(0);
	}

	const options = parseArgs(process.argv.slice(2));
	const summary = options.eventPks.length
		? await importFightOddsPks(options)
		: process.env.FIGHTODDS_RANGE_IMPORT === '1' || hasRangeArg(process.argv)
			? await importFightOddsRange(options)
			: await importFightOddsEvent(DEFAULT_EVENT_PK, { includeProps: options.includeProps });
	console.log(JSON.stringify(summary, null, 2));
}

export async function importFightOddsEvent(
	eventPk = DEFAULT_EVENT_PK,
	options: EventImportOptions = { includeProps: false },
): Promise<EventImportSummary> {
	const event = eventPk === DEFAULT_EVENT_PK ? DEFAULT_EVENT : await fetchEventIndexByPk(eventPk);
	if (!event) {
		throw new Error(`No FightOdds event found for pk=${eventPk}`);
	}
	return importFightOddsEventNode(event, options);
}

export async function importFightOddsRange(options: ImportOptions): Promise<RangeImportSummary> {
	const events = await fetchEventIndexRange(options);
	return importFightOddsEvents(events, options);
}

export async function importFightOddsPks(options: ImportOptions): Promise<RangeImportSummary> {
	const imported: EventImportSummary[] = [];
	const failedEvents: RangeImportSummary['failedEvents'] = [];
	for (const [index, eventPk] of options.eventPks.entries()) {
		try {
			const event = await fetchEventHeaderByPk(eventPk);
			imported.push(await importFightOddsEventNode({ ...event, pk: eventPk }, options));
		} catch (error) {
			if (!options.continueOnError) {
				throw error;
			}
			failedEvents.push({
				sourceEventId: String(eventPk),
				error: error instanceof Error ? error.message : String(error),
			});
		}
		if (index < options.eventPks.length - 1 && options.delayMs > 0) {
			await sleep(options.delayMs);
		}
	}
	return buildRangeImportSummary({
		options: { ...options, limit: options.eventPks.length },
		eventsScanned: options.eventPks.length,
		eventsSkipped: 0,
		imported,
		failedEvents,
	});
}

async function importFightOddsEvents(
	events: EventIndexNode[],
	options: ImportOptions,
): Promise<RangeImportSummary> {
	const imported: EventImportSummary[] = [];
	let eventsSkipped = 0;
	const failedEvents: RangeImportSummary['failedEvents'] = [];
	for (const [index, event] of events.entries()) {
		if (!isUfcEvent(event)) {
			eventsSkipped += 1;
			continue;
		}
		if (imported.length >= options.limit) {
			eventsSkipped += 1;
			continue;
		}
		try {
			imported.push(await importFightOddsEventNode(event, options));
		} catch (error) {
			if (!options.continueOnError) {
				throw error;
			}
			failedEvents.push({
				sourceEventId: String(event.pk),
				error: error instanceof Error ? error.message : String(error),
			});
		}
		if (index < events.length - 1 && options.delayMs > 0) {
			await sleep(options.delayMs);
		}
	}
	return buildRangeImportSummary({
		options,
		eventsScanned: events.length,
		eventsSkipped,
		imported,
		failedEvents,
	});
}

function buildRangeImportSummary(input: {
	options: ImportOptions;
	eventsScanned: number;
	eventsSkipped: number;
	imported: EventImportSummary[];
	failedEvents: RangeImportSummary['failedEvents'];
}): RangeImportSummary {
	return {
		source: SOURCE,
		from: input.options.from,
		to: input.options.to,
		limit: input.options.limit,
		delayMs: input.options.delayMs,
		eventsScanned: input.eventsScanned,
		eventsImported: input.imported.length,
		eventsSkipped: input.eventsSkipped,
		eventsFailed: input.failedEvents.length,
		fightsRead: sum(input.imported, 'fightsRead'),
		moneylinesRead: sum(input.imported, 'moneylinesRead'),
		propLinesRead: sum(input.imported, 'propLinesRead'),
		propLinesSkipped: sum(input.imported, 'propLinesSkipped'),
		propMarketsRead: sum(input.imported, 'propMarketsRead'),
		propMarketsImported: sum(input.imported, 'propMarketsImported'),
		propMarketsSkipped: sum(input.imported, 'propMarketsSkipped'),
		propSkippedMarketReasons: mergeReasonCounts(
			input.imported.map((event) => event.propSkippedMarketReasons),
		),
		matchedRows: sum(input.imported, 'matchedRows'),
		unmatchedRows: sum(input.imported, 'unmatchedRows'),
		skippedRows: sum(input.imported, 'skippedRows'),
		cancelledFights: sum(input.imported, 'cancelledFights'),
		sourceEventIds: input.imported.map((event) => event.sourceEventId),
		failedEvents: input.failedEvents,
	};
}

async function importFightOddsEventNode(
	event: EventIndexNode,
	options: EventImportOptions,
): Promise<EventImportSummary> {
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
	const propResult = options.includeProps
		? await buildPropOddsRows(sourceEventId, fights, scrapedAt)
		: emptyPropImportResult();
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
					includeProps: options.includeProps,
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
						includeProps: options.includeProps,
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

		for (const row of propResult.rows) {
			await tx
				.insert(historicalPropOdds)
				.values(row)
				.onConflictDoUpdate({
					target: historicalPropOdds.id,
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
		propLinesRead: propResult.rows.length,
		propLinesSkipped: propResult.skippedRows,
		propMarketsRead: propResult.marketsRead,
		propMarketsImported: propResult.marketsImported,
		propMarketsSkipped: propResult.marketsSkipped,
		propSkippedMarketReasons: propResult.skippedMarketReasons,
		rowsUpserted:
			1 + fights.length + moneylineRows.length + propResult.rows.length + unmatchedRows.length,
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
		eventPks: [],
		continueOnError: false,
		includeProps: false,
	});
	return events.find((event) => event.pk === eventPk) ?? null;
}

async function fetchEventHeaderByPk(eventPk: number): Promise<EventIndexNode> {
	const body = await graphql<EventHeaderData>({
		operationName: 'EventsHeaderEventQuery',
		variables: { eventPk },
		query: EVENT_HEADER_QUERY,
	});
	const event = body.event;
	if (!event) {
		throw new Error(`FightOdds EventsHeaderEventQuery returned no event for pk=${eventPk}`);
	}
	return event;
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

async function fetchFightPropOfferTable(slug: string): Promise<FightPropOfferTable | null> {
	const body = await graphql<FightPropOffersData>({
		operationName: 'FightPropOfferTableQuery',
		variables: { slug },
		query: FIGHT_PROP_OFFER_TABLE_QUERY,
	});
	return body.fightPropOfferTable ?? null;
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
		throw new Error(
			`FightOdds ${payload.operationName} failed with HTTP ${response.status} for variables ${stringifyJson(payload.variables)}`,
		);
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

function emptyPropImportResult(): PropImportResult {
	return {
		rows: [],
		skippedRows: 0,
		marketsRead: 0,
		marketsImported: 0,
		marketsSkipped: 0,
		skippedMarketReasons: {},
	};
}

async function buildPropOddsRows(
	sourceEventId: string,
	fights: FightOfferNode[],
	scrapedAt: Date,
): Promise<PropImportResult> {
	const result = emptyPropImportResult();
	for (const fight of fights) {
		if (fight.isCancelled || fight.propCount === 0) {
			incrementReason(
				result.skippedMarketReasons,
				fight.isCancelled ? 'cancelled_fight' : 'no_props',
			);
			result.marketsSkipped += 1;
			continue;
		}
		const propTable = await fetchFightPropOfferTable(fight.slug);
		if (!propTable) {
			incrementReason(result.skippedMarketReasons, 'missing_prop_table');
			result.marketsSkipped += 1;
			continue;
		}
		for (const edge of propTable.propOffers.edges) {
			const prop = edge.node;
			result.marketsRead += 1;
			if (prop.offerType.offerTypeId !== 'DISTANCE') {
				incrementReason(
					result.skippedMarketReasons,
					`ignored_offer_type:${prop.offerType.offerTypeId}`,
				);
				result.marketsSkipped += 1;
				continue;
			}
			const before = result.rows.length;
			for (const offerEdge of prop.offers.edges) {
				const offer = offerEdge.node;
				const outcome1 = propOutcomeRows({
					sourceEventId,
					fight,
					propTable,
					prop,
					offer,
					outcome: offer.outcome1,
					outcomeSide: 'outcome1',
					scrapedAt,
				});
				const outcome2 = propOutcomeRows({
					sourceEventId,
					fight,
					propTable,
					prop,
					offer,
					outcome: offer.outcome2,
					outcomeSide: 'outcome2',
					scrapedAt,
				});
				result.rows.push(...outcome1.rows, ...outcome2.rows);
				result.skippedRows += outcome1.skippedRows + outcome2.skippedRows;
			}
			if (result.rows.length > before) {
				result.marketsImported += 1;
			} else {
				incrementReason(result.skippedMarketReasons, 'distance_without_importable_lines');
				result.marketsSkipped += 1;
			}
		}
	}
	return result;
}

function propOutcomeRows(input: {
	sourceEventId: string;
	fight: FightOfferNode;
	propTable: FightPropOfferTable;
	prop: PropOfferNode;
	offer: PropSportsbookOfferNode;
	outcome: PropOutcome | null;
	outcomeSide: 'outcome1' | 'outcome2';
	scrapedAt: Date;
}): { rows: PropOddsRow[]; skippedRows: number } {
	const rows: PropOddsRow[] = [];
	let skippedRows = 0;
	if (input.outcome === null) {
		return { rows, skippedRows: 2 };
	}
	const rowInput = { ...input, outcome: input.outcome };
	if (input.outcome.odds !== null) {
		rows.push(propOddsRow(rowInput, input.outcome.odds, 'source_current'));
	} else {
		skippedRows += 1;
	}
	if (input.outcome.oddsPrev !== null) {
		rows.push(propOddsRow(rowInput, input.outcome.oddsPrev, 'source_previous'));
	} else {
		skippedRows += 1;
	}
	return { rows, skippedRows };
}

function propOddsRow(
	input: {
		sourceEventId: string;
		fight: FightOfferNode;
		propTable: FightPropOfferTable;
		prop: PropOfferNode;
		offer: PropSportsbookOfferNode;
		outcome: PropOutcome;
		outcomeSide: 'outcome1' | 'outcome2';
		scrapedAt: Date;
	},
	americanOdds: number,
	lineKind: 'source_current' | 'source_previous',
): PropOddsRow {
	const importRunId = importRunIdFor(input.sourceEventId);
	const sourceMarketId = propMarketId(input.fight, input.prop);
	return {
		id: stableId(
			SOURCE,
			'prop',
			importRunId,
			sourceMarketId,
			input.offer.id,
			input.outcome.id,
			lineKind,
		),
		importRunId,
		historicalFightId: fightId(input.sourceEventId, input.fight.id),
		sourceEventId: input.sourceEventId,
		sourceFightId: input.fight.id,
		sourceMarketId,
		sourceOfferId: input.offer.id,
		sourceOfferTypeId: input.prop.offerType.offerTypeId,
		marketFamily: 'fight_distance',
		marketLabel: input.prop.offerType.description,
		propName: input.outcomeSide === 'outcome1' ? input.prop.propName1 : input.prop.propName2,
		sportsbookId: input.offer.sportsbook.id,
		sportsbookSlug: input.offer.sportsbook.slug,
		sportsbookName: input.offer.sportsbook.shortName,
		sourceOutcomeId: input.outcome.id,
		rawOutcomeName: input.outcome.name,
		rawFighterName: input.outcome.fighter ? fighterName(input.outcome.fighter) : null,
		sourceFighterId: input.outcome.fighter?.id ?? null,
		canonicalFighterId: null,
		side: 'fight',
		outcomeSide: input.outcomeSide,
		isNot: input.outcome.isNot,
		lineKind,
		americanOdds,
		decimalOdds: americanToDecimal(americanOdds),
		impliedProbability: americanToImpliedProbability(americanOdds),
		marketTimestamp: null,
		marketTimestampSemantics:
			lineKind === 'source_current' ? 'source_current_at_scrape' : 'source_previous_unknown_time',
		scrapedAt: input.scrapedAt,
		rawMetadata: stringifyJson({
			fightSlug: input.fight.slug,
			propFight: input.propTable.fight,
			sourceMarketId,
			offerType: input.prop.offerType,
			propName1: input.prop.propName1,
			propName2: input.prop.propName2,
			bestOdds1: input.prop.bestOdds1,
			bestOdds2: input.prop.bestOdds2,
			offerId: input.offer.id,
			outcomeId: input.outcome.id,
			outcomeSide: input.outcomeSide,
			lineKind,
			odds: americanOdds,
			oddsOpen: input.outcome.oddsOpen,
			oddsBest: input.outcome.oddsBest,
			oddsWorst: input.outcome.oddsWorst,
			sportsbook: input.offer.sportsbook,
		}),
	};
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
		eventPks: parseEventPks(readArg(args, '--event-pks')),
		continueOnError: args.includes('--continue-on-error'),
		includeProps: args.includes('--include-props'),
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

function parseEventPks(value: string | null): number[] {
	if (!value) return [];
	return value.split(',').map((part) => {
		const eventPk = Number(part.trim());
		if (!Number.isInteger(eventPk)) {
			throw new Error(`Invalid event pk: ${part}`);
		}
		return eventPk;
	});
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

function propMarketId(fight: FightOfferNode, prop: PropOfferNode): string {
	return stableId(
		SOURCE,
		'prop-market',
		fight.id,
		prop.offerType.offerTypeId,
		prop.propName1,
		prop.propName2,
	);
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

function incrementReason(reasons: Record<string, number>, reason: string): void {
	reasons[reason] = (reasons[reason] ?? 0) + 1;
}

function mergeReasonCounts(rows: Array<Record<string, number>>): Record<string, number> {
	const merged: Record<string, number> = {};
	for (const row of rows) {
		for (const [reason, count] of Object.entries(row)) {
			merged[reason] = (merged[reason] ?? 0) + count;
		}
	}
	return merged;
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

const EVENT_HEADER_QUERY = `query EventsHeaderEventQuery($eventPk: Int) {
	event: eventByPk(pk: $eventPk) {
		id
		pk
		name
		slug
		date
		venue
		city
		promotion { id slug shortName }
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

const FIGHT_PROP_OFFER_TABLE_QUERY = `query FightPropOfferTableQuery($slug: String!) {
	fightPropOfferTable(slug: $slug) {
		id
		fight {
			id
			pk
			slug
			fighter1 { id firstName lastName slug }
			fighter2 { id firstName lastName slug }
			fightItdOdds
			fighter1ItdOdds
			fighter2ItdOdds
			fighter1KoOdds
			fighter2KoOdds
			fighter1SubOdds
			fighter2SubOdds
			fighter1DecOdds
			fighter2DecOdds
		}
		propOffers(first: 24) {
			edges {
				node {
					offerType {
						offerTypeId
						category
						subCategory
						description
						value
						notDescription
					}
					propName1
					propName2
					bestOdds1
					bestOdds2
					offers {
						edges {
							node {
								id
								sportsbook { id shortName slug }
								outcome1 {
									id
									name
									odds
									oddsPrev
									oddsOpen
									oddsBest
									oddsWorst
									isNot
									fighter { id firstName lastName slug }
								}
								outcome2 {
									id
									name
									odds
									oddsPrev
									oddsOpen
									oddsBest
									oddsWorst
									isNot
									fighter { id firstName lastName slug }
								}
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
