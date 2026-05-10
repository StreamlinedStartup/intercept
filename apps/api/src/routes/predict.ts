import { db, predictions, sql } from '@interceptor/db';
import type { Hono } from 'hono';
import { getBridge } from '../bridge';

type FightParticipantRow = {
	event_date: string | Date;
	fighter_id: string;
	backfill_status:
		| 'none'
		| 'current'
		| 'stale_count'
		| 'stale_stats'
		| 'in_progress'
		| 'failed'
		| null;
};

type MlPredictResult = {
	predicted_winner_id: string;
	win_prob: number;
	model_version: string;
	contributing_features?: Array<{
		name: string;
		value: number | null;
		shap: number;
	}>;
};

type EventFightRow = FightParticipantRow & {
	fight_id: string;
};

type StoredPrediction = {
	fight_id: string;
	fight_date: string;
	fighter_a_id: string;
	fighter_b_id: string;
	predicted_winner_id: string;
	win_prob: number;
	model_version: string;
	contributing_features: Array<{
		name: string;
		value: number | null;
		shap: number;
	}>;
	odds?: MarketOdds[];
	edge_pct?: number;
	market_prob?: number;
};

type MarketOdds = {
	fighter_id: string;
	decimal_odds: number;
	american_odds: number;
	market_prob: number;
};

export function registerPredictRoutes(app: Hono): void {
	app.get('/api/predict/fight/:id', async (c) => {
		const fightId = c.req.param('id');
		const rows = await loadFightParticipants(fightId);
		if (rows.length === 0) {
			return c.json({ error: 'Fight not found', fight_id: fightId }, 404);
		}
		if (rows.length !== 2) {
			return c.json(
				{
					error: 'Fight must have exactly two participants before prediction',
					fight_id: fightId,
					participant_count: rows.length,
				},
				409,
			);
		}

		const notCurrent = rows.filter((row) => row.backfill_status !== 'current');
		if (notCurrent.length > 0) {
			return c.json(
				{
					error: 'Both fighters must have current backfill state before prediction',
					fight_id: fightId,
					fighters: rows.map((row) => ({
						fighter_id: row.fighter_id,
						backfill_status: row.backfill_status ?? 'none',
					})),
				},
				409,
			);
		}

		return c.json(await predictAndPersist(fightId, rows));
	});

	app.get('/api/predict/event/:id', async (c) => {
		const eventId = c.req.param('id');
		const rows = await loadEventParticipants(eventId);
		if (rows.length === 0) {
			return c.json({ error: 'Event not found or has no fights', event_id: eventId }, 404);
		}

		const byFight = new Map<string, EventFightRow[]>();
		for (const row of rows) {
			byFight.set(row.fight_id, [...(byFight.get(row.fight_id) ?? []), row]);
		}

		const results: StoredPrediction[] = [];
		const skipped: Array<{
			fight_id: string;
			reason: string;
			fighters?: Array<{ fighter_id: string; backfill_status: string }>;
		}> = [];

		for (const [fightId, fightRows] of byFight) {
			if (fightRows.length !== 2) {
				skipped.push({
					fight_id: fightId,
					reason: 'fight must have exactly two participants before prediction',
				});
				continue;
			}

			const notCurrent = fightRows.filter((row) => row.backfill_status !== 'current');
			if (notCurrent.length > 0) {
				skipped.push({
					fight_id: fightId,
					reason: 'both fighters must have current backfill state before prediction',
					fighters: fightRows.map((row) => ({
						fighter_id: row.fighter_id,
						backfill_status: row.backfill_status ?? 'none',
					})),
				});
				continue;
			}

			results.push(await predictAndPersist(fightId, fightRows));
		}

		return c.json({ event_id: eventId, predictions: results, skipped });
	});
}

async function loadFightParticipants(fightId: string): Promise<FightParticipantRow[]> {
	return (await sql`
		SELECT
			e.date AS event_date,
			fr.fighter_id,
			fbs.status AS backfill_status
		FROM fights f
		JOIN events e ON e.id = f.event_id
		JOIN fight_results fr ON fr.fight_id = f.id
		LEFT JOIN fighter_backfill_state fbs ON fbs.fighter_id = fr.fighter_id
		WHERE f.id = ${fightId}
		ORDER BY fr.fighter_id ASC
	`) as FightParticipantRow[];
}

async function loadEventParticipants(eventId: string): Promise<EventFightRow[]> {
	return (await sql`
		SELECT
			f.id AS fight_id,
			e.date AS event_date,
			fr.fighter_id,
			fbs.status AS backfill_status
		FROM events e
		JOIN fights f ON f.event_id = e.id
		JOIN fight_results fr ON fr.fight_id = f.id
		LEFT JOIN fighter_backfill_state fbs ON fbs.fighter_id = fr.fighter_id
		WHERE e.id = ${eventId}
		ORDER BY f.id ASC, fr.fighter_id ASC
	`) as EventFightRow[];
}

async function predictAndPersist(
	fightId: string,
	rows: Array<{ event_date: string | Date; fighter_id: string }>,
): Promise<StoredPrediction> {
	const [fighterA, fighterB] = rows;
	const fightDate = formatDbDate(fighterA.event_date);
	const bridge = await getBridge();
	const result = await bridge.call<MlPredictResult>('ml.predict', {
		fighter_a_id: fighterA.fighter_id,
		fighter_b_id: fighterB.fighter_id,
		fight_date: fightDate,
	});
	const market = await loadMarketOdds(fightId);
	const predictedMarketOdds = market.find((odds) => odds.fighter_id === result.predicted_winner_id);
	const edgePct = predictedMarketOdds ? result.win_prob - predictedMarketOdds.market_prob : null;

	await db.insert(predictions).values({
		fightId,
		modelVersion: result.model_version,
		predictedAt: new Date(),
		predictedWinnerId: result.predicted_winner_id,
		winProb: result.win_prob,
		edgePct,
	});

	return {
		fight_id: fightId,
		fight_date: fightDate,
		fighter_a_id: fighterA.fighter_id,
		fighter_b_id: fighterB.fighter_id,
		predicted_winner_id: result.predicted_winner_id,
		win_prob: result.win_prob,
		model_version: result.model_version,
		contributing_features: result.contributing_features ?? [],
		...(market.length === 2 && edgePct !== null
			? { odds: market, edge_pct: edgePct, market_prob: predictedMarketOdds?.market_prob }
			: {}),
	};
}

async function loadMarketOdds(fightId: string): Promise<MarketOdds[]> {
	const rows = (await sql`
		WITH latest AS (
			SELECT max(snapshot_at) AS snapshot_at
			FROM odds_snapshots
			WHERE fight_id = ${fightId}
		),
		best AS (
			SELECT DISTINCT ON (o.fighter_id)
				o.fighter_id,
				o.decimal_odds,
				o.american_odds
			FROM odds_snapshots o
			JOIN latest l ON l.snapshot_at = o.snapshot_at
			WHERE o.fight_id = ${fightId}
			ORDER BY o.fighter_id ASC, o.decimal_odds DESC
		)
		SELECT fighter_id, decimal_odds, american_odds
		FROM best
	`) as Array<{
		fighter_id: string;
		decimal_odds: number;
		american_odds: number;
	}>;
	if (rows.length !== 2) return [];

	const raw = rows.map((row) => ({
		...row,
		rawMarketProb: 1 / row.decimal_odds,
	}));
	const total = raw.reduce((sum, row) => sum + row.rawMarketProb, 0);
	if (total <= 0) return [];

	return raw.map((row) => ({
		fighter_id: row.fighter_id,
		decimal_odds: row.decimal_odds,
		american_odds: row.american_odds,
		market_prob: row.rawMarketProb / total,
	}));
}

function formatDbDate(value: string | Date): string {
	if (value instanceof Date) return value.toISOString().slice(0, 10);
	return value;
}
