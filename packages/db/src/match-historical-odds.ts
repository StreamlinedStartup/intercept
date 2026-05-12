import { and, eq, gte, lte } from 'drizzle-orm';
import { db, sql } from './client.js';
import {
	type CanonicalFight,
	type FightMatch,
	matchHistoricalFight,
	normalizeName,
} from './match-historical-odds-core.js';
import {
	events,
	fighters,
	fightResults,
	fights,
	historicalMoneylineOdds,
	historicalOddsEvents,
	historicalOddsFights,
	unmatchedHistoricalOdds,
} from './schema.js';

type HistoricalEvent = typeof historicalOddsEvents.$inferSelect;
type HistoricalFight = typeof historicalOddsFights.$inferSelect;

type CanonicalEvent = {
	id: string;
	name: string;
	date: string;
	promotion: string;
};

type MatchSummary = {
	sourceEventId: string;
	canonicalEventId: string | null;
	fightsRead: number;
	fightsMatched: number;
	fightsAmbiguous: number;
	fightsUnmatched: number;
	cancelledUnmatched: number;
	moneylineRowsLinked: number;
	matchRate: number;
	unmatchedRate: number;
};

const SOURCE = 'fightodds';
const TARGET_EVENT_ID = '5362';

async function main() {
	try {
		const sourceEventIds = process.argv.includes('--all')
			? await listImportedSourceEventIds()
			: readSourceEventIds(process.argv.slice(2));
		const summaries = [];
		for (const sourceEventId of sourceEventIds) {
			summaries.push(await matchHistoricalOddsEvent(sourceEventId));
		}
		console.log(JSON.stringify(buildRangeSummary(summaries), null, 2));
	} finally {
		await sql.end();
	}
}

export async function matchHistoricalOddsEvent(sourceEventId: string): Promise<MatchSummary> {
	const [historicalEvent] = await db
		.select()
		.from(historicalOddsEvents)
		.where(
			and(
				eq(historicalOddsEvents.source, SOURCE),
				eq(historicalOddsEvents.sourceEventId, sourceEventId),
			),
		);
	if (!historicalEvent) {
		throw new Error(`No historical FightOdds event found for source_event_id=${sourceEventId}`);
	}

	const canonicalEventMatch = await findCanonicalEvent(historicalEvent);
	if (!canonicalEventMatch) {
		await markHistoricalEventUnmatched(
			historicalEvent,
			'no canonical event matched date/name/promotion',
		);
		return emptySummary(sourceEventId);
	}

	const historicalFights = await db
		.select()
		.from(historicalOddsFights)
		.where(eq(historicalOddsFights.historicalEventId, historicalEvent.id));
	const canonicalFights = await loadCanonicalFights(canonicalEventMatch.id);
	let fightsMatched = 0;
	let fightsAmbiguous = 0;
	let fightsUnmatched = 0;
	let cancelledUnmatched = 0;
	let moneylineRowsLinked = 0;

	await db
		.update(historicalOddsEvents)
		.set({
			canonicalEventId: canonicalEventMatch.id,
			matchStatus: 'matched',
			matchReason: canonicalEventMatch.reason,
			updatedAt: new Date(),
		})
		.where(eq(historicalOddsEvents.id, historicalEvent.id));

	for (const historicalFight of historicalFights) {
		const match = matchHistoricalFight(historicalFight, canonicalFights);
		if (match.status === 'matched') {
			fightsMatched += 1;
			await markFightMatched(historicalFight, match);
			moneylineRowsLinked += await linkMoneylines(historicalFight, match);
			continue;
		}

		if (match.status === 'ambiguous') {
			fightsAmbiguous += 1;
		} else {
			fightsUnmatched += 1;
			if (historicalFight.isCancelled) {
				cancelledUnmatched += 1;
			}
		}
		await markFightForReview(historicalEvent, historicalFight, match);
	}

	const fightsRead = historicalFights.length;
	return {
		sourceEventId,
		canonicalEventId: canonicalEventMatch.id,
		fightsRead,
		fightsMatched,
		fightsAmbiguous,
		fightsUnmatched,
		cancelledUnmatched,
		moneylineRowsLinked,
		matchRate: fightsRead === 0 ? 0 : fightsMatched / fightsRead,
		unmatchedRate: fightsRead === 0 ? 0 : (fightsAmbiguous + fightsUnmatched) / fightsRead,
	};
}

async function listImportedSourceEventIds(): Promise<string[]> {
	const rows = await db
		.select({ sourceEventId: historicalOddsEvents.sourceEventId })
		.from(historicalOddsEvents)
		.where(eq(historicalOddsEvents.source, SOURCE));
	return rows.map((row) => row.sourceEventId).sort((a, b) => Number(a) - Number(b));
}

function readSourceEventIds(args: string[]): string[] {
	const explicit = args.filter((arg) => !arg.startsWith('--'));
	return explicit.length > 0 ? explicit : [TARGET_EVENT_ID];
}

function buildRangeSummary(summaries: MatchSummary[]) {
	return {
		source: SOURCE,
		eventsMatched: summaries.filter((summary) => summary.canonicalEventId !== null).length,
		eventsRead: summaries.length,
		fightsRead: sum(summaries, 'fightsRead'),
		fightsMatched: sum(summaries, 'fightsMatched'),
		fightsAmbiguous: sum(summaries, 'fightsAmbiguous'),
		fightsUnmatched: sum(summaries, 'fightsUnmatched'),
		cancelledUnmatched: sum(summaries, 'cancelledUnmatched'),
		moneylineRowsLinked: sum(summaries, 'moneylineRowsLinked'),
		events: summaries,
	};
}

async function findCanonicalEvent(
	historicalEvent: HistoricalEvent,
): Promise<(CanonicalEvent & { reason: string }) | null> {
	const eventDate = new Date(`${historicalEvent.eventDate}T00:00:00Z`);
	const candidates = await db
		.select({
			id: events.id,
			name: events.name,
			date: events.date,
			promotion: events.promotion,
		})
		.from(events)
		.where(
			and(
				gte(events.date, dateString(addDays(eventDate, -1))),
				lte(events.date, dateString(addDays(eventDate, 1))),
				eq(events.promotion, 'ufc'),
			),
		);
	const historicalName = normalizeEventName(historicalEvent.rawName);
	const exact = candidates.find(
		(candidate) => normalizeEventName(candidate.name) === historicalName,
	);
	if (exact) {
		return {
			...exact,
			reason: 'matched by normalized event name, UFC promotion, and event date window',
		};
	}
	const tokenMatch = candidates.find((candidate) =>
		eventNameTokens(historicalName).every((token) =>
			normalizeEventName(candidate.name).includes(token),
		),
	);
	return tokenMatch
		? {
				...tokenMatch,
				reason: 'matched by event date, UFC promotion, and normalized headline tokens',
			}
		: null;
}

async function loadCanonicalFights(eventId: string): Promise<CanonicalFight[]> {
	const rows = await db
		.select({
			fightId: fights.id,
			weightClass: fights.weightClass,
			fighterId: fighters.id,
			fighterName: fighters.name,
		})
		.from(fights)
		.innerJoin(fightResults, eq(fightResults.fightId, fights.id))
		.innerJoin(fighters, eq(fighters.id, fightResults.fighterId))
		.where(eq(fights.eventId, eventId));
	const byFightId = new Map<string, CanonicalFight>();
	for (const row of rows) {
		const fight = byFightId.get(row.fightId) ?? {
			fightId: row.fightId,
			weightClass: row.weightClass,
			fighters: [],
		};
		fight.fighters.push({ id: row.fighterId, name: row.fighterName });
		byFightId.set(row.fightId, fight);
	}
	return [...byFightId.values()].filter((fight) => fight.fighters.length === 2);
}

async function markFightMatched(
	historicalFight: HistoricalFight,
	match: Extract<FightMatch, { status: 'matched' }>,
) {
	await db
		.update(historicalOddsFights)
		.set({
			canonicalFightId: match.fight.fightId,
			canonicalFighterAId: match.sourceFighterAToCanonicalId,
			canonicalFighterBId: match.sourceFighterBToCanonicalId,
			matchStatus: 'matched',
			matchReason: match.reason,
			candidateMatches: stringifyJson(candidateRows([match.fight])),
			updatedAt: new Date(),
		})
		.where(eq(historicalOddsFights.id, historicalFight.id));
	await db
		.delete(unmatchedHistoricalOdds)
		.where(
			and(
				eq(unmatchedHistoricalOdds.source, SOURCE),
				eq(unmatchedHistoricalOdds.sourceFightId, historicalFight.sourceFightId),
			),
		);
}

async function markFightForReview(
	historicalEvent: HistoricalEvent,
	historicalFight: HistoricalFight,
	match: Extract<FightMatch, { status: 'unmatched' | 'ambiguous' }>,
) {
	await db
		.update(historicalOddsFights)
		.set({
			canonicalFightId: null,
			canonicalFighterAId: null,
			canonicalFighterBId: null,
			matchStatus: match.status,
			matchReason: match.reason,
			candidateMatches: stringifyJson(candidateRows(match.candidates)),
			updatedAt: new Date(),
		})
		.where(eq(historicalOddsFights.id, historicalFight.id));
	await db
		.delete(unmatchedHistoricalOdds)
		.where(
			and(
				eq(unmatchedHistoricalOdds.source, SOURCE),
				eq(unmatchedHistoricalOdds.sourceEventId, historicalEvent.sourceEventId),
				eq(unmatchedHistoricalOdds.sourceFightId, historicalFight.sourceFightId),
			),
		);
	await db
		.insert(unmatchedHistoricalOdds)
		.values(reviewRow(historicalEvent, historicalFight, match.reason, match.candidates))
		.onConflictDoNothing();
}

async function linkMoneylines(
	historicalFight: HistoricalFight,
	match: Extract<FightMatch, { status: 'matched' }>,
) {
	const resultA = await db
		.update(historicalMoneylineOdds)
		.set({ canonicalFighterId: match.sourceFighterAToCanonicalId, updatedAt: new Date() })
		.where(
			and(
				eq(historicalMoneylineOdds.historicalFightId, historicalFight.id),
				eq(historicalMoneylineOdds.side, 'fighter_a'),
			),
		);
	const resultB = await db
		.update(historicalMoneylineOdds)
		.set({ canonicalFighterId: match.sourceFighterBToCanonicalId, updatedAt: new Date() })
		.where(
			and(
				eq(historicalMoneylineOdds.historicalFightId, historicalFight.id),
				eq(historicalMoneylineOdds.side, 'fighter_b'),
			),
		);
	return resultA.count + resultB.count;
}

async function markHistoricalEventUnmatched(historicalEvent: HistoricalEvent, reason: string) {
	await db
		.update(historicalOddsEvents)
		.set({
			canonicalEventId: null,
			matchStatus: 'unmatched',
			matchReason: reason,
			updatedAt: new Date(),
		})
		.where(eq(historicalOddsEvents.id, historicalEvent.id));
	const historicalFights = await db
		.select()
		.from(historicalOddsFights)
		.where(eq(historicalOddsFights.historicalEventId, historicalEvent.id));
	for (const historicalFight of historicalFights) {
		await db
			.update(historicalOddsFights)
			.set({
				canonicalFightId: null,
				canonicalFighterAId: null,
				canonicalFighterBId: null,
				matchStatus: 'unmatched',
				matchReason: reason,
				candidateMatches: stringifyJson([]),
				updatedAt: new Date(),
			})
			.where(eq(historicalOddsFights.id, historicalFight.id));
		await db
			.delete(unmatchedHistoricalOdds)
			.where(
				and(
					eq(unmatchedHistoricalOdds.source, SOURCE),
					eq(unmatchedHistoricalOdds.sourceEventId, historicalEvent.sourceEventId),
					eq(unmatchedHistoricalOdds.sourceFightId, historicalFight.sourceFightId),
				),
			);
		await db
			.insert(unmatchedHistoricalOdds)
			.values(reviewRow(historicalEvent, historicalFight, reason, []))
			.onConflictDoNothing();
	}
}

function emptySummary(sourceEventId: string): MatchSummary {
	return {
		sourceEventId,
		canonicalEventId: null,
		fightsRead: 0,
		fightsMatched: 0,
		fightsAmbiguous: 0,
		fightsUnmatched: 0,
		cancelledUnmatched: 0,
		moneylineRowsLinked: 0,
		matchRate: 0,
		unmatchedRate: 1,
	};
}

function normalizeEventName(value: string): string {
	return normalizeName(value).replace(/\bufc fight night \d+\b/, 'ufc fight night');
}

function eventNameTokens(normalizedEventName: string): string[] {
	return normalizedEventName
		.split(' ')
		.filter(
			(token) => !['ufc', 'fight', 'night', 'vs'].includes(token) && Number.isNaN(Number(token)),
		);
}

function candidateRows(candidates: CanonicalFight[]) {
	return candidates.map((candidate) => ({
		fightId: candidate.fightId,
		weightClass: candidate.weightClass ?? null,
		fighters: candidate.fighters,
	}));
}

function reviewRow(
	historicalEvent: HistoricalEvent,
	historicalFight: HistoricalFight,
	reason: string,
	candidates: CanonicalFight[],
): typeof unmatchedHistoricalOdds.$inferInsert {
	return {
		id: `${historicalFight.id}:match-review`,
		source: SOURCE,
		sourceEventId: historicalEvent.sourceEventId,
		sourceFightId: historicalFight.sourceFightId,
		sourceUrl: historicalFight.sourceUrl,
		rawEventName: historicalEvent.rawName,
		rawEventDate: historicalEvent.eventDate,
		rawFighterA: historicalFight.rawFighterA,
		rawFighterB: historicalFight.rawFighterB,
		rawSportsbook: null,
		rawOdds: historicalFight.rawMetadata,
		candidateMatches: stringifyJson(candidateRows(candidates)),
		reason,
		reviewed: false,
		reviewedAt: null,
		reviewNote: null,
	};
}

function addDays(date: Date, days: number): Date {
	const copy = new Date(date);
	copy.setUTCDate(copy.getUTCDate() + days);
	return copy;
}

function dateString(date: Date): string {
	return date.toISOString().slice(0, 10);
}

function stringifyJson(value: unknown): string {
	return JSON.stringify(value);
}

function sum(rows: MatchSummary[], key: keyof MatchSummary): number {
	return rows.reduce((total, row) => total + Number(row[key] ?? 0), 0);
}

if (process.argv[1]?.endsWith('match-historical-odds.ts')) {
	main().catch((error) => {
		console.error(error instanceof Error ? error.message : error);
		process.exit(1);
	});
}
