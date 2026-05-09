import {
	db,
	events,
	fighterBackfillState,
	fighterStatSnapshots,
	fighters,
	fightResults,
	fightRoundStats,
	fights,
	sql,
} from '@interceptor/db';
import type { Hono } from 'hono';
import {
	type BackfillJobProgress,
	getBackfillJob,
	serializeBackfillJob,
	startBackfillJob,
} from '../services/backfill-worker';

type UfcstatsFighter = {
	id: string;
	name: string;
	nickname: string | null;
	record: string;
	info: Record<string, string>;
	history: UfcstatsHistoryFight[];
	historyCount: number;
};

type UfcstatsHistoryFight = {
	fightId: string | null;
	result: string | null;
	fighters: Array<{ id: string | null; name: string }>;
	stats: {
		knockdowns: { self: string; opp: string };
		strikes: { self: string; opp: string };
		takedowns: { self: string; opp: string };
		submissions: { self: string; opp: string };
	};
	event: { id: string | null; name: string; date: string };
	method: string;
	methodDetail: string | null;
	round: string;
	time: string;
};

type UfcstatsFight = {
	id: string;
	bout: string;
	fighters: Array<{
		id: string | null;
		name: string;
		nickname: string | null;
		outcome: string | null;
	}>;
	summary: Record<string, string>;
	totals: Record<string, string> | null;
	totalsByRound: Array<{ round: string; data: Record<string, string> }>;
};

type Outcome = 'win' | 'loss' | 'draw' | 'nc';

type StoredBackfillState = {
	fighter_id: string;
	last_backfilled_at: Date | string | null;
	history_count_at_backfill: number;
	last_known_fight_id: string | null;
	status: 'none' | 'current' | 'stale_count' | 'stale_stats' | 'in_progress' | 'failed';
	last_error: string | null;
};

export function registerBackfillRoutes(app: Hono): void {
	app.get('/api/predict/backfill/job/:jobId', (c) => {
		const job = getBackfillJob(c.req.param('jobId'));
		if (!job) {
			return c.json({ error: 'Backfill job not found', status: 'failed' }, 404);
		}
		return c.json(serializeBackfillJob(job));
	});

	app.get('/api/predict/backfill/state/:fighterId', async (c) => {
		const fighterId = c.req.param('fighterId');
		if (!/^[a-f0-9]{16}$/i.test(fighterId)) {
			return c.json({ error: 'fighter id must be a 16-character hex string' }, 400);
		}

		const row = await getStoredBackfillState(fighterId);
		if (!row) {
			return c.json({
				fighter_id: fighterId,
				status: 'none',
				last_backfilled_at: null,
				history_count_at_backfill: 0,
				last_known_fight_id: null,
				last_error: null,
				new_fight_count: 0,
			});
		}

		if (row.status === 'current') {
			const origin = new URL(c.req.url).origin;
			const fighter = await fetchInternalJson<UfcstatsFighter>(
				origin,
				`/api/ufcstats/fighter/${fighterId}`,
			);
			const newFightCount = fighter.historyCount - row.history_count_at_backfill;
			if (newFightCount > 0) {
				return c.json(serializeBackfillState(row, 'stale_count', newFightCount));
			}
		}

		return c.json(serializeBackfillState(row, row.status, 0));
	});

	app.post('/api/predict/backfill/fighter/:id', async (c) => {
		const fighterId = c.req.param('id');
		if (!/^[a-f0-9]{16}$/i.test(fighterId)) {
			return c.json({ error: 'fighter id must be a 16-character hex string' }, 400);
		}

		const origin = new URL(c.req.url).origin;
		const job = startBackfillJob(fighterId, async ({ setProgress }) => {
			try {
				await runBackfill(fighterId, origin, setProgress);
			} catch (err) {
				await markBackfillFailed(fighterId, err);
				throw err;
			}
		});

		return c.json(serializeBackfillJob(job), 202);
	});
}

async function getStoredBackfillState(fighterId: string): Promise<StoredBackfillState | null> {
	const rows = await sql<StoredBackfillState[]>`
		SELECT
			fighter_id,
			last_backfilled_at,
			history_count_at_backfill,
			last_known_fight_id,
			status,
			last_error
		FROM fighter_backfill_state
		WHERE fighter_id = ${fighterId}
		LIMIT 1
	`;
	return rows[0] ?? null;
}

function serializeBackfillState(
	row: StoredBackfillState,
	status: StoredBackfillState['status'],
	newFightCount: number,
) {
	return {
		fighter_id: row.fighter_id,
		status,
		last_backfilled_at: row.last_backfilled_at,
		history_count_at_backfill: row.history_count_at_backfill,
		last_known_fight_id: row.last_known_fight_id,
		last_error: row.last_error,
		new_fight_count: newFightCount,
	};
}

async function runBackfill(
	fighterId: string,
	origin: string,
	setProgress: (progress: BackfillJobProgress) => void,
): Promise<void> {
	const previousState = await getStoredBackfillState(fighterId);
	const previousLastKnownFightId = previousState?.last_known_fight_id ?? null;
	setProgress({ current: 0, total: 0, message: 'Loading fighter profile' });
	const fighter = await fetchInternalJson<UfcstatsFighter>(
		origin,
		`/api/ufcstats/fighter/${fighterId}`,
	);
	const now = new Date();

	await upsertFighter(fighter);
	await markBackfillInProgress(fighter, previousState);
	await db
		.insert(fighterStatSnapshots)
		.values({
			fighterId: fighter.id,
			snapshotAt: now,
			slpm: parseNumber(fighter.info.slpm),
			strAcc: parsePercent(fighter.info.str_acc),
			sapm: parseNumber(fighter.info.sapm),
			strDef: parsePercent(fighter.info.str_def),
			tdAvg: parseNumber(fighter.info.td_avg),
			tdAcc: parsePercent(fighter.info.td_acc),
			tdDef: parsePercent(fighter.info.td_def),
			subAvg: parseNumber(fighter.info.sub_avg),
			...parseRecord(fighter.record),
		})
		.onConflictDoNothing();

	const validHistory = fighter.history.filter((fight) => fight.fightId && fight.event.id);
	const knownFightIndex = previousLastKnownFightId
		? validHistory.findIndex((fight) => fight.fightId === previousLastKnownFightId)
		: -1;
	const history =
		knownFightIndex >= 0 && previousState?.status !== 'none'
			? validHistory.slice(0, knownFightIndex)
			: validHistory;
	for (let i = 0; i < history.length; i++) {
		const historyFight = history[i];
		if (!historyFight.fightId) continue;
		setProgress({
			current: i + 1,
			total: history.length,
			message: `Loading fight ${i + 1} of ${history.length}`,
		});
		const fight = await fetchInternalJson<UfcstatsFight>(
			origin,
			`/api/ufcstats/fight/${historyFight.fightId}`,
		);
		await upsertFightFromHistory(historyFight, fight);
	}

	await markBackfillCurrent(fighter, now);
	setProgress({
		current: history.length,
		total: history.length,
		message: history.length > 0 ? 'Backfill complete' : 'Backfill already current',
	});
}

async function fetchInternalJson<T>(origin: string, path: string): Promise<T> {
	const res = await fetch(`${origin}${path}`);
	const text = await res.text();
	if (!res.ok) {
		throw new Error(`${path} returned ${res.status}: ${text.slice(0, 300)}`);
	}
	return JSON.parse(text) as T;
}

async function upsertFighter(fighter: UfcstatsFighter): Promise<void> {
	await db
		.insert(fighters)
		.values({
			id: fighter.id,
			name: fighter.name,
			nickname: fighter.nickname,
			dob: parseUfcstatsDate(fighter.info.dob),
			heightIn: parseHeightInches(fighter.info.height),
			reachIn: parseReachInches(fighter.info.reach),
			stance: fighter.info.stance?.toLowerCase() || null,
			historyCount: fighter.historyCount,
		})
		.onConflictDoUpdate({
			target: fighters.id,
			set: {
				name: fighter.name,
				nickname: fighter.nickname,
				dob: parseUfcstatsDate(fighter.info.dob),
				heightIn: parseHeightInches(fighter.info.height),
				reachIn: parseReachInches(fighter.info.reach),
				stance: fighter.info.stance?.toLowerCase() || null,
				historyCount: fighter.historyCount,
			},
		});
}

async function markBackfillInProgress(
	fighter: UfcstatsFighter,
	previousState: StoredBackfillState | null,
): Promise<void> {
	const lastKnownFightId =
		previousState?.last_known_fight_id ??
		fighter.history.find((fight) => fight.fightId)?.fightId ??
		null;
	await db
		.insert(fighterBackfillState)
		.values({
			fighterId: fighter.id,
			historyCountAtBackfill: previousState?.history_count_at_backfill ?? 0,
			lastKnownFightId,
			status: 'in_progress',
			lastError: null,
		})
		.onConflictDoUpdate({
			target: fighterBackfillState.fighterId,
			set: {
				historyCountAtBackfill: previousState?.history_count_at_backfill ?? 0,
				lastKnownFightId,
				status: 'in_progress',
				lastError: null,
			},
		});
}

async function markBackfillCurrent(
	fighter: UfcstatsFighter,
	lastBackfilledAt: Date,
): Promise<void> {
	const lastKnownFightId = fighter.history.find((fight) => fight.fightId)?.fightId ?? null;
	await db
		.insert(fighterBackfillState)
		.values({
			fighterId: fighter.id,
			lastBackfilledAt,
			historyCountAtBackfill: fighter.historyCount,
			lastKnownFightId,
			status: 'current',
			lastError: null,
		})
		.onConflictDoUpdate({
			target: fighterBackfillState.fighterId,
			set: {
				lastBackfilledAt,
				historyCountAtBackfill: fighter.historyCount,
				lastKnownFightId,
				status: 'current',
				lastError: null,
			},
		});
}

async function markBackfillFailed(fighterId: string, err: unknown): Promise<void> {
	const message = err instanceof Error ? err.message : String(err);
	await sql`
		UPDATE fighter_backfill_state
		SET status = 'failed', last_error = ${message}
		WHERE fighter_id = ${fighterId}
	`;
}

async function upsertMinimalFighter(fighter: {
	id: string | null;
	name: string;
	nickname?: string | null;
}): Promise<void> {
	if (!fighter.id) return;
	await db
		.insert(fighters)
		.values({
			id: fighter.id,
			name: fighter.name,
			nickname: fighter.nickname ?? null,
		})
		.onConflictDoUpdate({
			target: fighters.id,
			set: {
				name: fighter.name,
				nickname: fighter.nickname ?? null,
			},
		});
}
async function upsertFightFromHistory(
	historyFight: UfcstatsHistoryFight,
	fight: UfcstatsFight,
): Promise<{ fights: number; results: number; roundStats: number }> {
	if (!historyFight.fightId || !historyFight.event.id) {
		return { fights: 0, results: 0, roundStats: 0 };
	}

	for (const fighter of fight.fighters) {
		await upsertMinimalFighter(fighter);
	}
	for (const fighter of historyFight.fighters) {
		await upsertMinimalFighter(fighter);
	}

	await db
		.insert(events)
		.values({
			id: historyFight.event.id,
			name: historyFight.event.name,
			date: parseUfcstatsDate(historyFight.event.date) ?? '1970-01-01',
			location: null,
			completed: true,
			promotion: 'ufc',
		})
		.onConflictDoUpdate({
			target: events.id,
			set: {
				name: historyFight.event.name,
				date: parseUfcstatsDate(historyFight.event.date) ?? '1970-01-01',
				completed: true,
				promotion: 'ufc',
			},
		});

	await db
		.insert(fights)
		.values({
			id: historyFight.fightId,
			eventId: historyFight.event.id,
			weightClass: normalizeBout(fight.bout),
			scheduledRounds: parseScheduledRounds(fight.summary.time_format),
			isHeadliner: false,
		})
		.onConflictDoUpdate({
			target: fights.id,
			set: {
				eventId: historyFight.event.id,
				weightClass: normalizeBout(fight.bout),
				scheduledRounds: parseScheduledRounds(fight.summary.time_format),
			},
		});

	const fighterRows = fight.fighters.filter((fighter): fighter is typeof fighter & { id: string } =>
		Boolean(fighter.id),
	);
	let resultCount = 0;
	for (let i = 0; i < fighterRows.length; i++) {
		const row = fighterRows[i];
		const opponent = fighterRows.find((other) => other.id !== row.id);
		if (!opponent) continue;
		const totals = splitStatsForIndex(fight.totals, i);
		await db
			.insert(fightResults)
			.values({
				fightId: historyFight.fightId,
				fighterId: row.id,
				opponentId: opponent.id,
				outcome: normalizeOutcome(row.outcome),
				method: fight.summary.method || historyFight.method || null,
				methodDetail: fight.summary.details || historyFight.methodDetail || null,
				round: parseInteger(fight.summary.round || historyFight.round),
				timeSeconds: parseClockSeconds(fight.summary.time || historyFight.time),
				knockdowns: totals.knockdowns,
				sigStrikesLanded: totals.sigStrikesLanded,
				sigStrikesAttempted: totals.sigStrikesAttempted,
				totalStrikesLanded: totals.totalStrikesLanded,
				totalStrikesAttempted: totals.totalStrikesAttempted,
				takedownsLanded: totals.takedownsLanded,
				takedownsAttempted: totals.takedownsAttempted,
				subAttempts: totals.subAttempts,
				ctrlSeconds: totals.ctrlSeconds,
				reversals: totals.reversals,
			})
			.onConflictDoUpdate({
				target: [fightResults.fightId, fightResults.fighterId],
				set: {
					opponentId: opponent.id,
					outcome: normalizeOutcome(row.outcome),
					method: fight.summary.method || historyFight.method || null,
					methodDetail: fight.summary.details || historyFight.methodDetail || null,
					round: parseInteger(fight.summary.round || historyFight.round),
					timeSeconds: parseClockSeconds(fight.summary.time || historyFight.time),
					knockdowns: totals.knockdowns,
					sigStrikesLanded: totals.sigStrikesLanded,
					sigStrikesAttempted: totals.sigStrikesAttempted,
					totalStrikesLanded: totals.totalStrikesLanded,
					totalStrikesAttempted: totals.totalStrikesAttempted,
					takedownsLanded: totals.takedownsLanded,
					takedownsAttempted: totals.takedownsAttempted,
					subAttempts: totals.subAttempts,
					ctrlSeconds: totals.ctrlSeconds,
					reversals: totals.reversals,
				},
			});
		resultCount++;
	}

	let roundStatCount = 0;
	for (const round of fight.totalsByRound) {
		const roundNumber = parseInteger(round.round);
		if (!roundNumber) continue;
		for (let i = 0; i < fighterRows.length; i++) {
			const row = fighterRows[i];
			const stats = splitStatsForIndex(round.data, i);
			await db
				.insert(fightRoundStats)
				.values({
					fightId: historyFight.fightId,
					fighterId: row.id,
					round: roundNumber,
					knockdowns: stats.knockdowns,
					sigStrikesLanded: stats.sigStrikesLanded,
					sigStrikesAttempted: stats.sigStrikesAttempted,
					totalStrikesLanded: stats.totalStrikesLanded,
					totalStrikesAttempted: stats.totalStrikesAttempted,
					takedownsLanded: stats.takedownsLanded,
					takedownsAttempted: stats.takedownsAttempted,
					subAttempts: stats.subAttempts,
					ctrlSeconds: stats.ctrlSeconds,
					reversals: stats.reversals,
				})
				.onConflictDoUpdate({
					target: [fightRoundStats.fightId, fightRoundStats.fighterId, fightRoundStats.round],
					set: {
						knockdowns: stats.knockdowns,
						sigStrikesLanded: stats.sigStrikesLanded,
						sigStrikesAttempted: stats.sigStrikesAttempted,
						totalStrikesLanded: stats.totalStrikesLanded,
						totalStrikesAttempted: stats.totalStrikesAttempted,
						takedownsLanded: stats.takedownsLanded,
						takedownsAttempted: stats.takedownsAttempted,
						subAttempts: stats.subAttempts,
						ctrlSeconds: stats.ctrlSeconds,
						reversals: stats.reversals,
					},
				});
			roundStatCount++;
		}
	}

	return {
		fights: 1,
		results: resultCount,
		roundStats: roundStatCount,
	};
}

function parseRecord(record: string): {
	wins: number | null;
	losses: number | null;
	draws: number | null;
} {
	const match = record.match(/(\d+)-(\d+)-(\d+)/);
	return {
		wins: match ? Number.parseInt(match[1], 10) : null,
		losses: match ? Number.parseInt(match[2], 10) : null,
		draws: match ? Number.parseInt(match[3], 10) : null,
	};
}

function parseUfcstatsDate(value: string | undefined): string | null {
	if (!value || value === '--') return null;
	const cleaned = value.replace(/\./g, '');
	const date = new Date(cleaned);
	if (Number.isNaN(date.getTime())) return null;
	return date.toISOString().slice(0, 10);
}

function parseHeightInches(value: string | undefined): number | null {
	if (!value || value === '--') return null;
	const match = value.match(/(\d+)'\s*(\d+)/);
	if (!match) return null;
	return Number.parseInt(match[1], 10) * 12 + Number.parseInt(match[2], 10);
}

function parseReachInches(value: string | undefined): number | null {
	if (!value || value === '--') return null;
	const match = value.match(/(\d+)/);
	return match ? Number.parseInt(match[1], 10) : null;
}

function parsePercent(value: string | undefined): number | null {
	if (!value || value === '--') return null;
	const match = value.match(/-?\d+(\.\d+)?/);
	return match ? Number.parseFloat(match[0]) / 100 : null;
}

function parseNumber(value: string | undefined): number | null {
	if (!value || value === '--') return null;
	const match = value.match(/-?\d+(\.\d+)?/);
	return match ? Number.parseFloat(match[0]) : null;
}

function parseInteger(value: string | undefined): number | null {
	if (!value) return null;
	const match = value.match(/\d+/);
	return match ? Number.parseInt(match[0], 10) : null;
}

function parseClockSeconds(value: string | undefined): number | null {
	if (!value) return null;
	const match = value.match(/(\d+):(\d+)/);
	if (!match) return null;
	return Number.parseInt(match[1], 10) * 60 + Number.parseInt(match[2], 10);
}

function parseScheduledRounds(value: string | undefined): number | null {
	if (!value) return null;
	const match = value.match(/(\d+)\s*Rnd/i);
	return match ? Number.parseInt(match[1], 10) : null;
}

function normalizeBout(value: string): string | null {
	const normalized = value
		.replace(/\bUFC\b/gi, '')
		.replace(/\bBout\b/gi, '')
		.replace(/\s+/g, ' ')
		.trim()
		.toLowerCase();
	return normalized || null;
}

function normalizeOutcome(value: string | null): Outcome {
	const normalized = value?.toLowerCase();
	if (normalized === 'w' || normalized === 'win') return 'win';
	if (normalized === 'l' || normalized === 'loss') return 'loss';
	if (normalized === 'd' || normalized === 'draw') return 'draw';
	return 'nc';
}

function splitStatsForIndex(
	stats: Record<string, string> | null,
	index: number,
): {
	knockdowns: number | null;
	sigStrikesLanded: number | null;
	sigStrikesAttempted: number | null;
	totalStrikesLanded: number | null;
	totalStrikesAttempted: number | null;
	takedownsLanded: number | null;
	takedownsAttempted: number | null;
	subAttempts: number | null;
	ctrlSeconds: number | null;
	reversals: number | null;
} {
	return {
		knockdowns: parseInteger(pickSplit(stats, 'KD', index)),
		sigStrikesLanded: parseMadeAttempt(pickSplit(stats, 'SIG. STR.', index)).made,
		sigStrikesAttempted: parseMadeAttempt(pickSplit(stats, 'SIG. STR.', index)).attempt,
		totalStrikesLanded: parseMadeAttempt(pickSplit(stats, 'TOTAL STR.', index)).made,
		totalStrikesAttempted: parseMadeAttempt(pickSplit(stats, 'TOTAL STR.', index)).attempt,
		takedownsLanded: parseMadeAttempt(pickSplit(stats, 'TD', index)).made,
		takedownsAttempted: parseMadeAttempt(pickSplit(stats, 'TD', index)).attempt,
		subAttempts: parseInteger(pickSplit(stats, 'SUB. ATT', index)),
		ctrlSeconds: parseClockSeconds(pickSplit(stats, 'CTRL', index)),
		reversals: parseInteger(pickSplit(stats, 'REV.', index)),
	};
}

function pickSplit(
	stats: Record<string, string> | null,
	key: string,
	index: number,
): string | undefined {
	const value = stats?.[key];
	return value?.split('|')[index]?.trim();
}

function parseMadeAttempt(value: string | undefined): {
	made: number | null;
	attempt: number | null;
} {
	if (!value) return { made: null, attempt: null };
	const match = value.match(/(\d+)\s+of\s+(\d+)/i);
	if (!match) return { made: parseInteger(value), attempt: null };
	return {
		made: Number.parseInt(match[1], 10),
		attempt: Number.parseInt(match[2], 10),
	};
}
