import { eq } from 'drizzle-orm';
import { db, sql } from './client.js';
import {
	events,
	fighterBackfillState,
	fighterStatSnapshots,
	fighters,
	fightResults,
	fightRoundStats,
	fights,
	modelVersions,
	oddsSnapshots,
	predictions,
} from './schema.js';

const EVENT_ID = '9eedac48b497de5a';
const FIGHTER_A = '767755fd74662dbf';
const FIGHTER_B = '8a8b8c8d8e8f9091';
const FIGHT_ID = 'ffeeddccbbaa9988';
const NOW = new Date();
const MODEL_ID = 'smoke-model-v1';

await db
	.insert(events)
	.values({
		id: EVENT_ID,
		name: 'UFC 328',
		date: '2026-05-31',
		location: 'Las Vegas, Nevada, United States',
		completed: false,
		promotion: 'ufc',
	})
	.onConflictDoNothing();

await db
	.insert(fighters)
	.values([
		{
			id: FIGHTER_A,
			name: 'Khamzat Chimaev',
			nickname: 'Borz',
			dob: '1994-05-01',
			heightIn: 74,
			reachIn: 75,
			stance: 'orthodox',
			historyCount: 10,
		},
		{
			id: FIGHTER_B,
			name: 'Sean Strickland',
			nickname: 'Tarzan',
			dob: '1991-02-27',
			heightIn: 73,
			reachIn: 76,
			stance: 'orthodox',
			historyCount: 30,
		},
	])
	.onConflictDoNothing();

await db
	.insert(fighterBackfillState)
	.values({
		fighterId: FIGHTER_A,
		lastBackfilledAt: NOW,
		historyCountAtBackfill: 10,
		lastKnownFightId: FIGHT_ID,
		status: 'current',
	})
	.onConflictDoNothing();

await db
	.insert(fighterStatSnapshots)
	.values({
		fighterId: FIGHTER_A,
		snapshotAt: NOW,
		slpm: 4.2,
		strAcc: 0.55,
		ufcFightCount: 8,
		primaryWeightClass: 'middleweight',
	})
	.onConflictDoNothing();

await db
	.insert(fights)
	.values({
		id: FIGHT_ID,
		eventId: EVENT_ID,
		weightClass: 'middleweight',
		scheduledRounds: 5,
		isHeadliner: true,
	})
	.onConflictDoNothing();

await db
	.insert(fightResults)
	.values([
		{
			fightId: FIGHT_ID,
			fighterId: FIGHTER_A,
			opponentId: FIGHTER_B,
			outcome: 'win',
			method: 'Submission',
			round: 2,
			timeSeconds: 134,
		},
		{
			fightId: FIGHT_ID,
			fighterId: FIGHTER_B,
			opponentId: FIGHTER_A,
			outcome: 'loss',
			method: 'Submission',
			round: 2,
			timeSeconds: 134,
		},
	])
	.onConflictDoNothing();

await db
	.insert(fightRoundStats)
	.values({
		fightId: FIGHT_ID,
		fighterId: FIGHTER_A,
		round: 1,
		sigStrikesLanded: 12,
		sigStrikesAttempted: 30,
		takedownsLanded: 2,
	})
	.onConflictDoNothing();

await db
	.insert(oddsSnapshots)
	.values({
		eventId: EVENT_ID,
		fightId: FIGHT_ID,
		fighterId: FIGHTER_A,
		snapshotAt: NOW,
		bookmaker: 'draftkings',
		decimalOdds: 1.5,
		americanOdds: -200,
	})
	.onConflictDoNothing();

await db
	.insert(modelVersions)
	.values({
		id: MODEL_ID,
		trainedAt: NOW,
		trainingSetSize: 1000,
		accuracy: 0.65,
		logLoss: 0.62,
		brierScore: 0.21,
		rocAuc: 0.71,
		modelPath: 'data/models/smoke.json',
	})
	.onConflictDoNothing();

await db
	.insert(predictions)
	.values({
		fightId: FIGHT_ID,
		modelVersion: MODEL_ID,
		predictedAt: NOW,
		predictedWinnerId: FIGHTER_A,
		winProb: 0.62,
		edgePct: 0.04,
	})
	.onConflictDoNothing();

const checks: Array<[string, () => Promise<unknown>]> = [
	['events', () => db.select().from(events).where(eq(events.id, EVENT_ID))],
	['fighters', () => db.select().from(fighters).where(eq(fighters.id, FIGHTER_A))],
	[
		'fighter_backfill_state',
		() =>
			db.select().from(fighterBackfillState).where(eq(fighterBackfillState.fighterId, FIGHTER_A)),
	],
	[
		'fighter_stat_snapshots',
		() =>
			db.select().from(fighterStatSnapshots).where(eq(fighterStatSnapshots.fighterId, FIGHTER_A)),
	],
	['fights', () => db.select().from(fights).where(eq(fights.id, FIGHT_ID))],
	['fight_results', () => db.select().from(fightResults).where(eq(fightResults.fightId, FIGHT_ID))],
	[
		'fight_round_stats',
		() => db.select().from(fightRoundStats).where(eq(fightRoundStats.fightId, FIGHT_ID)),
	],
	[
		'odds_snapshots',
		() => db.select().from(oddsSnapshots).where(eq(oddsSnapshots.fightId, FIGHT_ID)),
	],
	['model_versions', () => db.select().from(modelVersions).where(eq(modelVersions.id, MODEL_ID))],
	['predictions', () => db.select().from(predictions).where(eq(predictions.fightId, FIGHT_ID))],
];

for (const [name, run] of checks) {
	const rows = (await run()) as unknown[];
	if (!rows.length) throw new Error(`${name}: round-trip failed (0 rows)`);
	console.log(`[smoke] ${name}: ${rows.length} row(s)`);
}

console.log('[smoke] ok — all 10 tables round-tripped');
await sql.end();
