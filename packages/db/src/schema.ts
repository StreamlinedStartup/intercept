import {
	boolean,
	date,
	integer,
	pgEnum,
	pgTable,
	primaryKey,
	real,
	text,
	timestamp,
} from 'drizzle-orm/pg-core';

export const promotionEnum = pgEnum('promotion', ['ufc', 'bellator', 'strikeforce', 'other']);

export const backfillStatusEnum = pgEnum('backfill_status', [
	'none',
	'current',
	'stale_count',
	'stale_stats',
	'in_progress',
	'failed',
]);

export const outcomeEnum = pgEnum('outcome', ['win', 'loss', 'draw', 'nc']);

export const events = pgTable('events', {
	id: text('id').primaryKey(),
	name: text('name').notNull(),
	date: date('date').notNull(),
	location: text('location'),
	completed: boolean('completed').notNull().default(false),
	promotion: promotionEnum('promotion').notNull().default('ufc'),
});

export const fighters = pgTable('fighters', {
	id: text('id').primaryKey(),
	name: text('name').notNull(),
	nickname: text('nickname'),
	dob: date('dob'),
	heightIn: real('height_in'),
	reachIn: real('reach_in'),
	stance: text('stance'),
	historyCount: integer('history_count').notNull().default(0),
});

export const fighterBackfillState = pgTable('fighter_backfill_state', {
	fighterId: text('fighter_id')
		.primaryKey()
		.references(() => fighters.id, { onDelete: 'cascade' }),
	lastBackfilledAt: timestamp('last_backfilled_at', { withTimezone: true }),
	historyCountAtBackfill: integer('history_count_at_backfill').notNull().default(0),
	lastKnownFightId: text('last_known_fight_id'),
	status: backfillStatusEnum('status').notNull().default('none'),
	lastError: text('last_error'),
});

export const fighterStatSnapshots = pgTable(
	'fighter_stat_snapshots',
	{
		fighterId: text('fighter_id')
			.notNull()
			.references(() => fighters.id, { onDelete: 'cascade' }),
		snapshotAt: timestamp('snapshot_at', { withTimezone: true }).notNull(),
		slpm: real('slpm'),
		strAcc: real('str_acc'),
		sapm: real('sapm'),
		strDef: real('str_def'),
		tdAvg: real('td_avg'),
		tdAcc: real('td_acc'),
		tdDef: real('td_def'),
		subAvg: real('sub_avg'),
		wins: integer('wins'),
		losses: integer('losses'),
		draws: integer('draws'),
		ufcFightCount: integer('ufc_fight_count'),
		daysSinceLastFight: integer('days_since_last_fight'),
		primaryWeightClass: text('primary_weight_class'),
	},
	(t) => ({
		pk: primaryKey({ columns: [t.fighterId, t.snapshotAt] }),
	}),
);

export const fights = pgTable('fights', {
	id: text('id').primaryKey(),
	eventId: text('event_id')
		.notNull()
		.references(() => events.id, { onDelete: 'cascade' }),
	weightClass: text('weight_class'),
	scheduledRounds: integer('scheduled_rounds'),
	isHeadliner: boolean('is_headliner').notNull().default(false),
});

export const fightResults = pgTable(
	'fight_results',
	{
		fightId: text('fight_id')
			.notNull()
			.references(() => fights.id, { onDelete: 'cascade' }),
		fighterId: text('fighter_id')
			.notNull()
			.references(() => fighters.id, { onDelete: 'cascade' }),
		opponentId: text('opponent_id')
			.notNull()
			.references(() => fighters.id, { onDelete: 'cascade' }),
		outcome: outcomeEnum('outcome').notNull(),
		method: text('method'),
		methodDetail: text('method_detail'),
		round: integer('round'),
		timeSeconds: integer('time_seconds'),
		knockdowns: integer('knockdowns'),
		sigStrikesLanded: integer('sig_strikes_landed'),
		sigStrikesAttempted: integer('sig_strikes_attempted'),
		totalStrikesLanded: integer('total_strikes_landed'),
		totalStrikesAttempted: integer('total_strikes_attempted'),
		takedownsLanded: integer('takedowns_landed'),
		takedownsAttempted: integer('takedowns_attempted'),
		subAttempts: integer('sub_attempts'),
		ctrlSeconds: integer('ctrl_seconds'),
		reversals: integer('reversals'),
	},
	(t) => ({
		pk: primaryKey({ columns: [t.fightId, t.fighterId] }),
	}),
);

export const fightRoundStats = pgTable(
	'fight_round_stats',
	{
		fightId: text('fight_id')
			.notNull()
			.references(() => fights.id, { onDelete: 'cascade' }),
		fighterId: text('fighter_id')
			.notNull()
			.references(() => fighters.id, { onDelete: 'cascade' }),
		round: integer('round').notNull(),
		knockdowns: integer('knockdowns'),
		sigStrikesLanded: integer('sig_strikes_landed'),
		sigStrikesAttempted: integer('sig_strikes_attempted'),
		totalStrikesLanded: integer('total_strikes_landed'),
		totalStrikesAttempted: integer('total_strikes_attempted'),
		takedownsLanded: integer('takedowns_landed'),
		takedownsAttempted: integer('takedowns_attempted'),
		subAttempts: integer('sub_attempts'),
		ctrlSeconds: integer('ctrl_seconds'),
		reversals: integer('reversals'),
	},
	(t) => ({
		pk: primaryKey({ columns: [t.fightId, t.fighterId, t.round] }),
	}),
);

export const oddsSnapshots = pgTable(
	'odds_snapshots',
	{
		eventId: text('event_id').references(() => events.id, {
			onDelete: 'set null',
		}),
		fightId: text('fight_id').references(() => fights.id, {
			onDelete: 'set null',
		}),
		fighterId: text('fighter_id')
			.notNull()
			.references(() => fighters.id, { onDelete: 'cascade' }),
		snapshotAt: timestamp('snapshot_at', { withTimezone: true }).notNull(),
		bookmaker: text('bookmaker').notNull(),
		decimalOdds: real('decimal_odds').notNull(),
		americanOdds: integer('american_odds').notNull(),
	},
	(t) => ({
		pk: primaryKey({
			columns: [t.fighterId, t.snapshotAt, t.bookmaker],
		}),
	}),
);

export const unmatchedOdds = pgTable('unmatched_odds', {
	id: text('id').primaryKey(),
	rawEventName: text('raw_event_name').notNull(),
	rawFighterA: text('raw_fighter_a').notNull(),
	rawFighterB: text('raw_fighter_b').notNull(),
	rawDate: date('raw_date').notNull(),
	snapshotId: text('snapshot_id').notNull(),
	reason: text('reason').notNull(),
	createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
});

export const modelVersions = pgTable('model_versions', {
	id: text('id').primaryKey(),
	trainedAt: timestamp('trained_at', { withTimezone: true }).notNull(),
	trainingSetSize: integer('training_set_size').notNull(),
	accuracy: real('accuracy'),
	logLoss: real('log_loss'),
	brierScore: real('brier_score'),
	rocAuc: real('roc_auc'),
	modelPath: text('model_path').notNull(),
	featureImportance: text('feature_importance'),
});

export const predictions = pgTable(
	'predictions',
	{
		fightId: text('fight_id')
			.notNull()
			.references(() => fights.id, { onDelete: 'cascade' }),
		modelVersion: text('model_version')
			.notNull()
			.references(() => modelVersions.id, { onDelete: 'cascade' }),
		predictedAt: timestamp('predicted_at', { withTimezone: true }).notNull(),
		predictedWinnerId: text('predicted_winner_id')
			.notNull()
			.references(() => fighters.id, { onDelete: 'cascade' }),
		winProb: real('win_prob').notNull(),
		edgePct: real('edge_pct'),
	},
	(t) => ({
		pk: primaryKey({
			columns: [t.fightId, t.modelVersion, t.predictedAt],
		}),
	}),
);
