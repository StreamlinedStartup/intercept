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

		const [fighterA, fighterB] = rows;
		const fightDate = formatDbDate(fighterA.event_date);
		const bridge = await getBridge();
		const result = await bridge.call<MlPredictResult>('ml.predict', {
			fighter_a_id: fighterA.fighter_id,
			fighter_b_id: fighterB.fighter_id,
			fight_date: fightDate,
		});

		await db.insert(predictions).values({
			fightId,
			modelVersion: result.model_version,
			predictedAt: new Date(),
			predictedWinnerId: result.predicted_winner_id,
			winProb: result.win_prob,
			edgePct: null,
		});

		return c.json({
			fight_id: fightId,
			fight_date: fightDate,
			fighter_a_id: fighterA.fighter_id,
			fighter_b_id: fighterB.fighter_id,
			predicted_winner_id: result.predicted_winner_id,
			win_prob: result.win_prob,
			model_version: result.model_version,
			contributing_features: result.contributing_features ?? [],
		});
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

function formatDbDate(value: string | Date): string {
	if (value instanceof Date) return value.toISOString().slice(0, 10);
	return value;
}
