import {
	boolean,
	date,
	index,
	integer,
	pgEnum,
	pgTable,
	primaryKey,
	real,
	text,
	timestamp,
	uniqueIndex,
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

export const historicalOddsImportRuns = pgTable('historical_odds_import_runs', {
	id: text('id').primaryKey(),
	source: text('source').notNull(),
	sourceUrl: text('source_url').notNull(),
	sourceEventId: text('source_event_id').notNull(),
	startedAt: timestamp('started_at', { withTimezone: true }).notNull(),
	finishedAt: timestamp('finished_at', { withTimezone: true }),
	status: text('status').notNull(),
	eventsRead: integer('events_read').notNull().default(0),
	fightsRead: integer('fights_read').notNull().default(0),
	moneylinesRead: integer('moneylines_read').notNull().default(0),
	matchedRows: integer('matched_rows').notNull().default(0),
	unmatchedRows: integer('unmatched_rows').notNull().default(0),
	rawMetadata: text('raw_metadata').notNull(),
});

export const historicalOddsEvents = pgTable(
	'historical_odds_events',
	{
		id: text('id').primaryKey(),
		source: text('source').notNull(),
		sourceEventId: text('source_event_id').notNull(),
		sourceEventGlobalId: text('source_event_global_id'),
		sourceSlug: text('source_slug').notNull(),
		sourceUrl: text('source_url').notNull(),
		rawName: text('raw_name').notNull(),
		eventDate: date('event_date').notNull(),
		venue: text('venue'),
		city: text('city'),
		promotion: text('promotion').notNull(),
		canonicalEventId: text('canonical_event_id').references(() => events.id, {
			onDelete: 'set null',
		}),
		matchStatus: text('match_status').notNull(),
		matchReason: text('match_reason').notNull(),
		rawMetadata: text('raw_metadata').notNull(),
		scrapedAt: timestamp('scraped_at', { withTimezone: true }).notNull(),
		createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
	},
	(t) => ({
		sourceEventIdx: uniqueIndex('historical_odds_events_source_event_idx').on(
			t.source,
			t.sourceEventId,
		),
	}),
);

export const historicalOddsFights = pgTable(
	'historical_odds_fights',
	{
		id: text('id').primaryKey(),
		historicalEventId: text('historical_event_id')
			.notNull()
			.references(() => historicalOddsEvents.id, { onDelete: 'cascade' }),
		sourceFightId: text('source_fight_id').notNull(),
		sourceFightSlug: text('source_fight_slug').notNull(),
		sourceUrl: text('source_url').notNull(),
		rawFighterA: text('raw_fighter_a').notNull(),
		rawFighterB: text('raw_fighter_b').notNull(),
		sourceFighterAId: text('source_fighter_a_id').notNull(),
		sourceFighterBId: text('source_fighter_b_id').notNull(),
		sourceFighterASlug: text('source_fighter_a_slug').notNull(),
		sourceFighterBSlug: text('source_fighter_b_slug').notNull(),
		isCancelled: boolean('is_cancelled').notNull().default(false),
		propCount: integer('prop_count').notNull().default(0),
		bestOddsA: integer('best_odds_a'),
		bestOddsB: integer('best_odds_b'),
		canonicalFightId: text('canonical_fight_id').references(() => fights.id, {
			onDelete: 'set null',
		}),
		canonicalFighterAId: text('canonical_fighter_a_id').references(() => fighters.id, {
			onDelete: 'set null',
		}),
		canonicalFighterBId: text('canonical_fighter_b_id').references(() => fighters.id, {
			onDelete: 'set null',
		}),
		matchStatus: text('match_status').notNull(),
		matchReason: text('match_reason').notNull(),
		candidateMatches: text('candidate_matches').notNull(),
		rawMetadata: text('raw_metadata').notNull(),
		scrapedAt: timestamp('scraped_at', { withTimezone: true }).notNull(),
		createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
	},
	(t) => ({
		sourceFightIdx: uniqueIndex('historical_odds_fights_source_fight_idx').on(
			t.historicalEventId,
			t.sourceFightId,
		),
	}),
);

export const historicalMoneylineOdds = pgTable(
	'historical_moneyline_odds',
	{
		id: text('id').primaryKey(),
		importRunId: text('import_run_id')
			.notNull()
			.references(() => historicalOddsImportRuns.id, { onDelete: 'cascade' }),
		historicalFightId: text('historical_fight_id')
			.notNull()
			.references(() => historicalOddsFights.id, { onDelete: 'cascade' }),
		sourceOfferId: text('source_offer_id').notNull(),
		sportsbookId: text('sportsbook_id').notNull(),
		sportsbookSlug: text('sportsbook_slug').notNull(),
		sportsbookName: text('sportsbook_name').notNull(),
		sourceOutcomeId: text('source_outcome_id').notNull(),
		rawFighterName: text('raw_fighter_name').notNull(),
		sourceFighterId: text('source_fighter_id').notNull(),
		canonicalFighterId: text('canonical_fighter_id').references(() => fighters.id, {
			onDelete: 'set null',
		}),
		side: text('side').notNull(),
		lineKind: text('line_kind').notNull(),
		americanOdds: integer('american_odds').notNull(),
		decimalOdds: real('decimal_odds').notNull(),
		impliedProbability: real('implied_probability').notNull(),
		marketTimestamp: timestamp('market_timestamp', { withTimezone: true }),
		marketTimestampSemantics: text('market_timestamp_semantics').notNull(),
		scrapedAt: timestamp('scraped_at', { withTimezone: true }).notNull(),
		rawMetadata: text('raw_metadata').notNull(),
		createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
	},
	(t) => ({
		sourceOutcomeIdx: uniqueIndex('historical_moneyline_odds_source_outcome_idx').on(
			t.importRunId,
			t.sourceOfferId,
			t.sourceOutcomeId,
			t.lineKind,
		),
	}),
);

export const historicalPropOdds = pgTable(
	'historical_prop_odds',
	{
		id: text('id').primaryKey(),
		importRunId: text('import_run_id')
			.notNull()
			.references(() => historicalOddsImportRuns.id, { onDelete: 'cascade' }),
		historicalFightId: text('historical_fight_id')
			.notNull()
			.references(() => historicalOddsFights.id, { onDelete: 'cascade' }),
		sourceEventId: text('source_event_id').notNull(),
		sourceFightId: text('source_fight_id').notNull(),
		sourceMarketId: text('source_market_id').notNull(),
		sourceOfferId: text('source_offer_id').notNull(),
		sourceOfferTypeId: text('source_offer_type_id').notNull(),
		marketFamily: text('market_family').notNull(),
		marketLabel: text('market_label').notNull(),
		propName: text('prop_name').notNull(),
		sportsbookId: text('sportsbook_id').notNull(),
		sportsbookSlug: text('sportsbook_slug').notNull(),
		sportsbookName: text('sportsbook_name').notNull(),
		sourceOutcomeId: text('source_outcome_id').notNull(),
		rawOutcomeName: text('raw_outcome_name').notNull(),
		rawFighterName: text('raw_fighter_name'),
		sourceFighterId: text('source_fighter_id'),
		canonicalFighterId: text('canonical_fighter_id').references(() => fighters.id, {
			onDelete: 'set null',
		}),
		side: text('side').notNull(),
		outcomeSide: text('outcome_side').notNull(),
		isNot: boolean('is_not').notNull().default(false),
		lineKind: text('line_kind').notNull(),
		americanOdds: integer('american_odds').notNull(),
		decimalOdds: real('decimal_odds').notNull(),
		impliedProbability: real('implied_probability').notNull(),
		marketTimestamp: timestamp('market_timestamp', { withTimezone: true }),
		marketTimestampSemantics: text('market_timestamp_semantics').notNull(),
		scrapedAt: timestamp('scraped_at', { withTimezone: true }).notNull(),
		rawMetadata: text('raw_metadata').notNull(),
		createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
	},
	(t) => ({
		sourceOutcomeIdx: uniqueIndex('historical_prop_odds_source_outcome_idx').on(
			t.importRunId,
			t.sourceMarketId,
			t.sourceOfferId,
			t.sourceOutcomeId,
			t.lineKind,
		),
	}),
);

export const unmatchedHistoricalOdds = pgTable('unmatched_historical_odds', {
	id: text('id').primaryKey(),
	source: text('source').notNull(),
	sourceEventId: text('source_event_id').notNull(),
	sourceFightId: text('source_fight_id').notNull(),
	sourceUrl: text('source_url').notNull(),
	rawEventName: text('raw_event_name').notNull(),
	rawEventDate: date('raw_event_date').notNull(),
	rawFighterA: text('raw_fighter_a').notNull(),
	rawFighterB: text('raw_fighter_b').notNull(),
	rawSportsbook: text('raw_sportsbook'),
	rawOdds: text('raw_odds').notNull(),
	candidateMatches: text('candidate_matches').notNull(),
	reason: text('reason').notNull(),
	reviewed: boolean('reviewed').notNull().default(false),
	reviewedAt: timestamp('reviewed_at', { withTimezone: true }),
	reviewNote: text('review_note'),
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

export const marketIndicatorSnapshots = pgTable(
	'market_indicator_snapshots',
	{
		fightId: text('fight_id')
			.notNull()
			.references(() => fights.id, { onDelete: 'cascade' }),
		target: text('target').notNull(),
		modelVersion: text('model_version').notNull(),
		indicatorName: text('indicator_name').notNull(),
		computedAt: timestamp('computed_at', { withTimezone: true }).notNull(),
		modelProbability: real('model_probability').notNull(),
		marketProbability: real('market_probability'),
		edgePct: real('edge_pct'),
		candidate: boolean('candidate').notNull().default(false),
		marketPairCount: integer('market_pair_count').notNull().default(0),
		valueStatus: text('value_status').notNull().default('research_only'),
		sourceReport: text('source_report').notNull(),
		sourceConfig: text('source_config'),
		sourceGitSha: text('source_git_sha'),
		sourceModelPath: text('source_model_path'),
		sourceDataWindow: text('source_data_window'),
		stalenessReason: text('staleness_reason'),
		rawMetadata: text('raw_metadata').notNull().default('{}'),
		createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
		updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
	},
	(t) => ({
		pk: primaryKey({
			columns: [t.fightId, t.target, t.modelVersion, t.indicatorName],
		}),
		fightTargetComputedAtIdx: index('market_indicator_snapshots_fight_target_computed_at_idx').on(
			t.fightId,
			t.target,
			t.computedAt,
		),
		valueStatusComputedAtIdx: index('market_indicator_snapshots_value_status_computed_at_idx').on(
			t.valueStatus,
			t.computedAt,
		),
	}),
);
