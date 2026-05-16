import { db, predictions, sql } from '@interceptor/db';
import type { Hono } from 'hono';
import { getBridge } from '../bridge';

type FightParticipantRow = {
	event_date: string | Date;
	weight_class: string | null;
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
	decision_signals?: DecisionSignals;
};

type MlOver25IndicatorResult = {
	target: 'over_2_5';
	label: string;
	model_version: string;
	model_probability: number | null;
	threshold: number;
	candidate: boolean;
	value_status: 'report_only' | 'insufficient_training';
	value_status_reason: string;
	training_sample_count: number;
};

type DecisionSignal = {
	label: string;
	summary: string;
	advantage: 'fighter_a' | 'fighter_b' | 'neutral';
};

type DecisionSignals = {
	round_tendency?: DecisionSignal;
	common_opponents?: DecisionSignal;
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
	decision_signals?: DecisionSignals;
	odds?: MarketOdds[];
	edge_pct?: number;
	market_prob?: number;
	over_2_5_indicator?: Over25Indicator;
	value_status: ValueStatus;
	value_status_reason: string;
};

type MarketOdds = {
	fighter_id: string;
	decimal_odds: number;
	american_odds: number;
	market_prob: number;
};

type ValueStatus = 'research_only' | 'insufficient_coverage' | 'validated';

type Over25Indicator = {
	target: 'over_2_5';
	label: string;
	model_version: string;
	model_probability: number | null;
	market_probability: number | null;
	edge_pct: number | null;
	threshold: number;
	candidate: boolean;
	market_pair_count: number;
	training_sample_count: number;
	value_status: 'report_only' | 'insufficient_coverage' | 'insufficient_training';
	value_status_reason: string;
};

type PredictionHistoryRow = {
	fight_id: string;
	event_name: string;
	event_date: string | Date;
	predicted_at: string | Date;
	predicted_winner_id: string;
	predicted_winner_name: string;
	win_prob: number;
	market_prob: number | null;
	edge_pct: number | null;
	actual_winner_id: string | null;
	actual_winner_name: string | null;
	best_decimal_odds: number | null;
};

type MlTrainResult = {
	model_id: string;
	model_path: string;
	training_set_size: number;
	train_rows: number;
	holdout_rows: number;
	log_loss: number;
	brier_score: number;
	accuracy: number;
	roc_auc: number;
	top_features: Array<{
		name: string;
		importance: number;
	}>;
};

type TrainJob = {
	jobId: string;
	status: 'in_progress' | 'completed' | 'failed';
	progress: { current: number; total: number; message: string };
	result: MlTrainResult | null;
	error: string | null;
	startedAt: string;
	completedAt: string | null;
};

const trainJobs = new Map<string, TrainJob>();

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

	app.get('/api/predict/history', async (c) => {
		const url = new URL(c.req.url);
		const from = url.searchParams.get('from');
		const to = url.searchParams.get('to');
		const rawLimit = Number.parseInt(url.searchParams.get('limit') ?? '100', 10);
		const limit = Number.isFinite(rawLimit) ? Math.max(1, Math.min(rawLimit, 500)) : 100;
		const rows = await loadPredictionHistory({ from, to, limit });
		const serialized = rows.map(serializeHistoryRow);
		return c.json({ aggregate: aggregateHistory(serialized), rows: serialized });
	});

	app.post('/api/predict/train', async (c) => {
		const unauthorized = requireAdmin(c.req.header('X-Admin-Secret'));
		if (unauthorized) return c.json(unauthorized.body, unauthorized.status);

		const job = startTrainJob();
		return c.json(serializeTrainJob(job), 202);
	});

	app.get('/api/predict/train/job/:id', (c) => {
		const unauthorized = requireAdmin(c.req.header('X-Admin-Secret'));
		if (unauthorized) return c.json(unauthorized.body, unauthorized.status);

		const jobId = c.req.param('id');
		const job = trainJobs.get(jobId);
		if (!job) return c.json({ error: 'Training job not found', job_id: jobId }, 404);
		return c.json(serializeTrainJob(job));
	});
}

function requireAdmin(secret: string | undefined): {
	body: { error: string };
	status: 401 | 500;
} | null {
	const expected = process.env.ADMIN_SECRET;
	if (!expected) return { body: { error: 'ADMIN_SECRET is not configured' }, status: 500 };
	if (!secret || secret !== expected)
		return { body: { error: 'Invalid admin secret' }, status: 401 };
	return null;
}

function startTrainJob(): TrainJob {
	const job: TrainJob = {
		jobId: crypto.randomUUID(),
		status: 'in_progress',
		progress: { current: 0, total: 3, message: 'Starting training' },
		result: null,
		error: null,
		startedAt: new Date().toISOString(),
		completedAt: null,
	};
	trainJobs.set(job.jobId, job);

	void (async () => {
		job.progress = { current: 1, total: 3, message: 'Training model' };
		const bridge = await getBridge();
		job.result = await bridge.call<MlTrainResult>('ml.train', {});
		job.progress = { current: 3, total: 3, message: 'Training complete' };
		job.status = 'completed';
		job.completedAt = new Date().toISOString();
	})().catch((err) => {
		job.status = 'failed';
		job.error = err instanceof Error ? err.message : String(err);
		job.progress = { current: job.progress.current, total: 3, message: 'Training failed' };
		job.completedAt = new Date().toISOString();
	});

	return job;
}

function serializeTrainJob(job: TrainJob) {
	return {
		job_id: job.jobId,
		status: job.status,
		progress: job.progress,
		result: job.result,
		error: job.error,
		started_at: job.startedAt,
		completed_at: job.completedAt,
	};
}

async function loadFightParticipants(fightId: string): Promise<FightParticipantRow[]> {
	return (await sql`
		SELECT
			e.date AS event_date,
			f.weight_class,
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
			f.weight_class,
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
	rows: Array<{ event_date: string | Date; weight_class: string | null; fighter_id: string }>,
): Promise<StoredPrediction> {
	const [fighterA, fighterB] = rows;
	const fightDate = formatDbDate(fighterA.event_date);
	const bridge = await getBridge();
	const result = await bridge.call<MlPredictResult>(
		'ml.predict',
		buildMlPredictParams(fighterA, fighterB),
	);
	const over25Result = await bridge.call<MlOver25IndicatorResult>(
		'ml.prop_indicator.over_2_5',
		buildMlPredictParams(fighterA, fighterB),
	);
	const market = await loadMarketOdds(fightId);
	const over25Market = await loadOver25Market(fightId);
	const predictedMarketOdds = market.find((odds) => odds.fighter_id === result.predicted_winner_id);
	const edgePct = predictedMarketOdds ? result.win_prob - predictedMarketOdds.market_prob : null;
	const over25Indicator = mergeOver25Indicator(over25Result, over25Market);

	await db.insert(predictions).values({
		fightId,
		modelVersion: result.model_version,
		predictedAt: new Date(),
		predictedWinnerId: result.predicted_winner_id,
		winProb: result.win_prob,
		edgePct,
	});

	const valueStatus = getValueStatus(market.length === 2 && edgePct !== null);

	return {
		fight_id: fightId,
		fight_date: fightDate,
		fighter_a_id: fighterA.fighter_id,
		fighter_b_id: fighterB.fighter_id,
		predicted_winner_id: result.predicted_winner_id,
		win_prob: result.win_prob,
		model_version: result.model_version,
		contributing_features: result.contributing_features ?? [],
		...(result.decision_signals ? { decision_signals: result.decision_signals } : {}),
		...(market.length === 2 && edgePct !== null
			? { odds: market, edge_pct: edgePct, market_prob: predictedMarketOdds?.market_prob }
			: {}),
		over_2_5_indicator: over25Indicator,
		value_status: valueStatus.status,
		value_status_reason: valueStatus.reason,
	};
}

export function getValueStatus(hasMatchedMarketOdds: boolean): {
	status: ValueStatus;
	reason: string;
} {
	if (!hasMatchedMarketOdds) {
		return {
			status: 'insufficient_coverage',
			reason: 'Matched two-sided market odds are required before edge can be evaluated.',
		};
	}
	return {
		status: 'research_only',
		reason:
			'Edge and ROI are simulated research metrics until leakage audits, baselines, and market-gated validation pass.',
	};
}

export function buildMlPredictParams(
	fighterA: { event_date: string | Date; weight_class: string | null; fighter_id: string },
	fighterB: { fighter_id: string },
): {
	fighter_a_id: string;
	fighter_b_id: string;
	fight_date: string;
	weight_class: string | null;
} {
	const fightDate = formatDbDate(fighterA.event_date);
	return {
		fighter_a_id: fighterA.fighter_id,
		fighter_b_id: fighterB.fighter_id,
		fight_date: fightDate,
		weight_class: fighterA.weight_class,
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

async function loadOver25Market(fightId: string): Promise<{
	market_probability: number;
	pair_count: number;
} | null> {
	const rows = (await sql`
		SELECT
			hpo.source_market_id,
			hpo.sportsbook_slug,
			hpo.outcome_side,
			hpo.implied_probability
		FROM historical_prop_odds hpo
		JOIN historical_odds_fights hof ON hof.id = hpo.historical_fight_id
		WHERE hof.canonical_fight_id = ${fightId}
			AND hpo.source_offer_type_id = 'OVERUNDER_2.5'
			AND hpo.line_kind = 'source_current'
	`) as Array<{
		source_market_id: string;
		sportsbook_slug: string;
		outcome_side: string;
		implied_probability: number;
	}>;
	return over25NoVigMarket(rows);
}

export function over25NoVigMarket(
	rows: Array<{
		source_market_id: string;
		sportsbook_slug: string;
		outcome_side: string;
		implied_probability: number;
	}>,
): { market_probability: number; pair_count: number } | null {
	const pairs = new Map<string, { outcome1?: number; outcome2?: number }>();
	for (const row of rows) {
		const key = `${row.source_market_id}:${row.sportsbook_slug}`;
		const pair = pairs.get(key) ?? {};
		if (row.outcome_side === 'outcome1') pair.outcome1 = Number(row.implied_probability);
		if (row.outcome_side === 'outcome2') pair.outcome2 = Number(row.implied_probability);
		pairs.set(key, pair);
	}
	const probabilities: number[] = [];
	for (const pair of pairs.values()) {
		if (pair.outcome1 === undefined || pair.outcome2 === undefined) continue;
		const total = pair.outcome1 + pair.outcome2;
		if (total > 0) probabilities.push(pair.outcome1 / total);
	}
	if (probabilities.length === 0) return null;
	return {
		market_probability: probabilities.reduce((sum, value) => sum + value, 0) / probabilities.length,
		pair_count: probabilities.length,
	};
}

export function mergeOver25Indicator(
	model: MlOver25IndicatorResult,
	market: { market_probability: number; pair_count: number } | null,
): Over25Indicator {
	if (model.value_status === 'insufficient_training' || model.model_probability === null) {
		return {
			target: 'over_2_5',
			label: model.label,
			model_version: model.model_version,
			model_probability: model.model_probability,
			market_probability: market?.market_probability ?? null,
			edge_pct:
				model.model_probability !== null && market
					? model.model_probability - market.market_probability
					: null,
			threshold: model.threshold,
			candidate: false,
			market_pair_count: market?.pair_count ?? 0,
			training_sample_count: model.training_sample_count,
			value_status: 'insufficient_training',
			value_status_reason: model.value_status_reason,
		};
	}
	if (!market) {
		return {
			target: 'over_2_5',
			label: model.label,
			model_version: model.model_version,
			model_probability: model.model_probability,
			market_probability: null,
			edge_pct: null,
			threshold: model.threshold,
			candidate: model.candidate,
			market_pair_count: 0,
			training_sample_count: model.training_sample_count,
			value_status: 'insufficient_coverage',
			value_status_reason:
				'Matched OVERUNDER_2.5 prop market is required before edge can be evaluated.',
		};
	}
	return {
		target: 'over_2_5',
		label: model.label,
		model_version: model.model_version,
		model_probability: model.model_probability,
		market_probability: market.market_probability,
		edge_pct: model.model_probability - market.market_probability,
		threshold: model.threshold,
		candidate: model.candidate,
		market_pair_count: market.pair_count,
		training_sample_count: model.training_sample_count,
		value_status: 'report_only',
		value_status_reason: model.value_status_reason,
	};
}

async function loadPredictionHistory({
	from,
	to,
	limit,
}: {
	from: string | null;
	to: string | null;
	limit: number;
}): Promise<PredictionHistoryRow[]> {
	return (await sql`
		WITH actual_winners AS (
			SELECT
				fr.fight_id,
				fr.fighter_id AS actual_winner_id,
				f.name AS actual_winner_name
			FROM fight_results fr
			JOIN fighters f ON f.id = fr.fighter_id
			WHERE fr.outcome = 'win'
		),
		best_odds AS (
			SELECT DISTINCT ON (fight_id, fighter_id)
				fight_id,
				fighter_id,
				decimal_odds
			FROM odds_snapshots
			ORDER BY fight_id, fighter_id, snapshot_at DESC, decimal_odds DESC
		)
		SELECT
			p.fight_id,
			e.name AS event_name,
			e.date AS event_date,
			p.predicted_at,
			p.predicted_winner_id,
			pf.name AS predicted_winner_name,
			p.win_prob,
			p.edge_pct,
			CASE WHEN p.edge_pct IS NULL THEN NULL ELSE p.win_prob - p.edge_pct END AS market_prob,
			aw.actual_winner_id,
			aw.actual_winner_name,
			bo.decimal_odds AS best_decimal_odds
		FROM predictions p
		JOIN fights fi ON fi.id = p.fight_id
		JOIN events e ON e.id = fi.event_id
		JOIN fighters pf ON pf.id = p.predicted_winner_id
		LEFT JOIN actual_winners aw ON aw.fight_id = p.fight_id
		LEFT JOIN best_odds bo
			ON bo.fight_id = p.fight_id
			AND bo.fighter_id = p.predicted_winner_id
		WHERE (${from}::date IS NULL OR e.date >= ${from}::date)
			AND (${to}::date IS NULL OR e.date <= ${to}::date)
		ORDER BY e.date DESC, p.predicted_at DESC
		LIMIT ${limit}
	`) as PredictionHistoryRow[];
}

type SerializedHistoryRow = {
	fight_id: string;
	event_name: string;
	event_date: string;
	predicted_at: string;
	predicted_winner_id: string;
	predicted_winner_name: string;
	win_prob: number;
	market_prob: number | null;
	edge_pct: number | null;
	actual_winner_id: string | null;
	actual_winner_name: string | null;
	hit: boolean | null;
	bet_pl_units: number | null;
	simulated_pl_units: number | null;
	value_status: ValueStatus;
	value_status_reason: string;
};

function serializeHistoryRow(row: PredictionHistoryRow): SerializedHistoryRow {
	const hit = row.actual_winner_id ? row.actual_winner_id === row.predicted_winner_id : null;
	const betPlaced = typeof row.edge_pct === 'number' && row.edge_pct > 0.05;
	const betPlUnits =
		betPlaced && hit !== null ? (hit ? (row.best_decimal_odds ?? 2) - 1 : -1) : null;
	const valueStatus = getValueStatus(row.market_prob !== null && row.edge_pct !== null);
	return {
		fight_id: row.fight_id,
		event_name: row.event_name,
		event_date: formatDbDate(row.event_date),
		predicted_at: formatDbTimestamp(row.predicted_at),
		predicted_winner_id: row.predicted_winner_id,
		predicted_winner_name: row.predicted_winner_name,
		win_prob: row.win_prob,
		market_prob: row.market_prob,
		edge_pct: row.edge_pct,
		actual_winner_id: row.actual_winner_id,
		actual_winner_name: row.actual_winner_name,
		hit,
		bet_pl_units: betPlUnits,
		simulated_pl_units: betPlUnits,
		value_status: valueStatus.status,
		value_status_reason: valueStatus.reason,
	};
}

function aggregateHistory(rows: SerializedHistoryRow[]): {
	n_predictions: number;
	n_with_result: number;
	accuracy: number | null;
	log_loss: number | null;
	brier: number | null;
	n_bets: number;
	roi_units: number;
	roi_pct: number | null;
	n_simulated_entries: number;
	simulated_roi_units: number;
	simulated_roi_pct: number | null;
	value_status: ValueStatus;
	value_status_reason: string;
} {
	const withResult = rows.filter((row) => row.hit !== null);
	const hits = withResult.filter((row) => row.hit).length;
	const probabilities = withResult.map((row) => (row.hit ? row.win_prob : 1 - row.win_prob));
	const bets = rows.filter((row) => row.bet_pl_units !== null);
	const roiUnits = bets.reduce((sum, row) => sum + (row.bet_pl_units ?? 0), 0);
	return {
		n_predictions: rows.length,
		n_with_result: withResult.length,
		accuracy: withResult.length ? hits / withResult.length : null,
		log_loss: probabilities.length
			? probabilities.reduce(
					(sum, probability) => sum - Math.log(clampProbability(probability)),
					0,
				) / probabilities.length
			: null,
		brier: probabilities.length
			? probabilities.reduce((sum, probability) => sum + (1 - probability) ** 2, 0) /
				probabilities.length
			: null,
		n_bets: bets.length,
		roi_units: roiUnits,
		roi_pct: bets.length ? roiUnits / bets.length : null,
		n_simulated_entries: bets.length,
		simulated_roi_units: roiUnits,
		simulated_roi_pct: bets.length ? roiUnits / bets.length : null,
		value_status: 'research_only',
		value_status_reason:
			'Prediction-history ROI is simulated research output until leakage audits, baselines, and market-gated validation pass.',
	};
}

function clampProbability(value: number): number {
	return Math.max(0.000001, Math.min(0.999999, value));
}

function formatDbDate(value: string | Date): string {
	if (value instanceof Date) return value.toISOString().slice(0, 10);
	return value;
}

function formatDbTimestamp(value: string | Date): string {
	if (value instanceof Date) return value.toISOString();
	return value;
}
