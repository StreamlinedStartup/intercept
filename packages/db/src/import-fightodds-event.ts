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
const TARGET_EVENT_PK = 5362;
const TARGET_EVENT_ID = String(TARGET_EVENT_PK);
const TARGET_EVENT_NAME = 'UFC Fight Night 237: Moreno vs. Royval 2';
const TARGET_EVENT_DATE = '2024-02-24';
const TARGET_EVENT_SLUG = 'ufc-fight-night-237-moreno-vs-royval-2';
const TARGET_EVENT_URL = `https://fightodds.io/mma-events/${TARGET_EVENT_PK}/${TARGET_EVENT_SLUG}/odds`;
const IMPORT_RUN_ID = `${SOURCE}:${TARGET_EVENT_ID}:single-event-moneyline`;

type GraphqlResponse = {
	data?: {
		eventOfferTable?: EventOfferTable | null;
	};
	errors?: unknown;
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
	outcome1: SourceOutcome;
	outcome2: SourceOutcome;
};

type SourceOutcome = {
	id: string;
	odds: number | null;
	oddsPrev: number | null;
};

type MoneylineRow = typeof historicalMoneylineOdds.$inferInsert;

type ImportSummary = {
	source: typeof SOURCE;
	sourceEventId: string;
	sourceUrl: string;
	eventsRead: number;
	fightsRead: number;
	moneylinesRead: number;
	rowsUpserted: number;
	matchedRows: number;
	unmatchedRows: number;
	cancelledFights: number;
};

function usage() {
	console.log(`Usage: pnpm --filter @interceptor/db import:fightodds:event

Imports only UFC Fight Night 237 / Moreno vs Royval 2 moneyline odds from FightOdds.
No event-list pagination or many-event scraping is performed.`);
}

async function main() {
	if (process.argv.includes('--help') || process.argv.includes('-h')) {
		usage();
		process.exit(0);
	}

	const summary = await importFightOddsEvent();
	console.log(JSON.stringify(summary, null, 2));
}

export async function importFightOddsEvent(): Promise<ImportSummary> {
	const startedAt = new Date();
	const scrapedAt = startedAt;
	const eventOfferTable = await fetchTargetEvent();
	if (eventOfferTable.pk !== TARGET_EVENT_PK) {
		throw new Error(`Expected FightOdds event ${TARGET_EVENT_PK}; received ${eventOfferTable.pk}`);
	}

	const eventId = stableId(SOURCE, 'event', TARGET_EVENT_ID);
	const fights = eventOfferTable.fightOffers.edges.map((edge) => edge.node);
	const moneylineRows = buildMoneylineRows(eventId, fights, scrapedAt);
	const unmatchedRows = fights.map((fight) => ({
		id: stableId(SOURCE, 'unmatched', TARGET_EVENT_ID, fight.id),
		source: SOURCE,
		sourceEventId: TARGET_EVENT_ID,
		sourceFightId: fight.id,
		sourceUrl: fightUrl(fight.slug),
		rawEventName: TARGET_EVENT_NAME,
		rawEventDate: TARGET_EVENT_DATE,
		rawFighterA: fighterName(fight.fighter1),
		rawFighterB: fighterName(fight.fighter2),
		rawSportsbook: null,
		rawOdds: stringifyJson({
			bestOdds1: fight.bestOdds1,
			bestOdds2: fight.bestOdds2,
			straightOfferCount: fight.straightOffers.edges.length,
		}),
		candidateMatches: stringifyJson([]),
		reason: 'canonical matching deferred to intercept-gopa',
		reviewed: false,
		reviewedAt: null,
		reviewNote: null,
	}));
	const finishedAt = new Date();
	const matchedRows = 0;
	const unmatchedRowCount = fights.length;

	await db.transaction(async (tx) => {
		await tx
			.insert(historicalOddsImportRuns)
			.values({
				id: IMPORT_RUN_ID,
				source: SOURCE,
				sourceUrl: TARGET_EVENT_URL,
				sourceEventId: TARGET_EVENT_ID,
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
					variables: { eventPk: TARGET_EVENT_PK },
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
						variables: { eventPk: TARGET_EVENT_PK },
					}),
				},
			});

		await tx
			.insert(historicalOddsEvents)
			.values({
				id: eventId,
				source: SOURCE,
				sourceEventId: TARGET_EVENT_ID,
				sourceEventGlobalId: eventOfferTable.id,
				sourceSlug: eventOfferTable.slug,
				sourceUrl: TARGET_EVENT_URL,
				rawName: TARGET_EVENT_NAME,
				eventDate: TARGET_EVENT_DATE,
				venue: 'Arena CDMX',
				city: 'Mexico City, Mexico',
				promotion: 'UFC',
				canonicalEventId: null,
				matchStatus: 'unmatched',
				matchReason: 'canonical matching deferred to intercept-gopa',
				rawMetadata: stringifyJson({
					pk: eventOfferTable.pk,
					id: eventOfferTable.id,
					slug: eventOfferTable.slug,
				}),
				scrapedAt,
				updatedAt: finishedAt,
			})
			.onConflictDoUpdate({
				target: historicalOddsEvents.id,
				set: {
					sourceEventGlobalId: eventOfferTable.id,
					sourceSlug: eventOfferTable.slug,
					rawMetadata: stringifyJson({
						pk: eventOfferTable.pk,
						id: eventOfferTable.id,
						slug: eventOfferTable.slug,
					}),
					scrapedAt,
					updatedAt: finishedAt,
				},
			});

		for (const fight of fights) {
			await tx
				.insert(historicalOddsFights)
				.values({
					id: fightId(fight.id),
					historicalEventId: eventId,
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
					matchReason: 'canonical matching deferred to intercept-gopa',
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

	await sql.end();

	return {
		source: SOURCE,
		sourceEventId: TARGET_EVENT_ID,
		sourceUrl: TARGET_EVENT_URL,
		eventsRead: 1,
		fightsRead: fights.length,
		moneylinesRead: moneylineRows.length,
		rowsUpserted: 1 + fights.length + moneylineRows.length + unmatchedRows.length,
		matchedRows,
		unmatchedRows: unmatchedRowCount,
		cancelledFights: fights.filter((fight) => fight.isCancelled).length,
	};
}

async function fetchTargetEvent(): Promise<EventOfferTable> {
	const response = await fetch('https://api.fightodds.io/gql', {
		method: 'POST',
		headers: { 'content-type': 'application/json' },
		body: JSON.stringify({
			operationName: 'EventOddsQuery',
			variables: { eventPk: TARGET_EVENT_PK },
			query: `query EventOddsQuery($eventPk: Int!) {
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
			}`,
		}),
	});

	if (!response.ok) {
		throw new Error(`FightOdds EventOddsQuery failed with HTTP ${response.status}`);
	}

	const body = (await response.json()) as GraphqlResponse;
	if (body.errors) {
		throw new Error(`FightOdds EventOddsQuery returned errors: ${stringifyJson(body.errors)}`);
	}
	const eventOfferTable = body.data?.eventOfferTable;
	if (!eventOfferTable) {
		throw new Error('FightOdds EventOddsQuery returned no eventOfferTable');
	}
	return eventOfferTable;
}

function buildMoneylineRows(
	historicalEventId: string,
	fights: FightOfferNode[],
	scrapedAt: Date,
): MoneylineRow[] {
	const rows: MoneylineRow[] = [];
	for (const fight of fights) {
		for (const edge of fight.straightOffers.edges) {
			const offer = edge.node;
			rows.push(
				...outcomeRows({
					historicalFightId: fightId(fight.id),
					offer,
					fighter: fight.fighter1,
					rawFighterName: fighterName(fight.fighter1),
					side: 'fighter_a',
					outcome: offer.outcome1,
					scrapedAt,
				}),
				...outcomeRows({
					historicalFightId: fightId(fight.id),
					offer,
					fighter: fight.fighter2,
					rawFighterName: fighterName(fight.fighter2),
					side: 'fighter_b',
					outcome: offer.outcome2,
					scrapedAt,
				}),
			);
		}
	}
	if (!historicalEventId) {
		throw new Error('historicalEventId is required');
	}
	return rows;
}

function outcomeRows(input: {
	historicalFightId: string;
	offer: StraightOfferNode;
	fighter: SourceFighter;
	rawFighterName: string;
	side: 'fighter_a' | 'fighter_b';
	outcome: SourceOutcome;
	scrapedAt: Date;
}): MoneylineRow[] {
	const rows: MoneylineRow[] = [];
	if (input.outcome.odds !== null) {
		rows.push(moneylineRow(input, input.outcome.odds, 'source_current'));
	}
	if (input.outcome.oddsPrev !== null) {
		rows.push(moneylineRow(input, input.outcome.oddsPrev, 'source_previous'));
	}
	return rows;
}

function moneylineRow(
	input: {
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
	return {
		id: stableId(SOURCE, 'moneyline', IMPORT_RUN_ID, input.offer.id, input.outcome.id, lineKind),
		importRunId: IMPORT_RUN_ID,
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

function fightId(sourceFightId: string): string {
	return stableId(SOURCE, 'fight', TARGET_EVENT_ID, sourceFightId);
}

function fightUrl(slug: string): string {
	return `https://fightodds.io/mma-bouts/${slug}/odds`;
}

function fighterName(fighter: SourceFighter): string {
	return `${fighter.firstName} ${fighter.lastName}`.trim();
}

function stableId(...parts: string[]): string {
	return createHash('sha256').update(parts.join('\0')).digest('hex').slice(0, 32);
}

function stringifyJson(value: unknown): string {
	return JSON.stringify(value);
}

if (process.argv[1]?.endsWith('import-fightodds-event.ts')) {
	main().catch((error) => {
		console.error(error instanceof Error ? error.message : error);
		process.exit(1);
	});
}
