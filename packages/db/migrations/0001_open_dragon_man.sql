CREATE TYPE "public"."backfill_status" AS ENUM('none', 'current', 'stale_count', 'stale_stats', 'in_progress', 'failed');--> statement-breakpoint
CREATE TYPE "public"."outcome" AS ENUM('win', 'loss', 'draw', 'nc');--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "fight_results" (
	"fight_id" varchar(16) NOT NULL,
	"fighter_id" varchar(16) NOT NULL,
	"opponent_id" varchar(16) NOT NULL,
	"outcome" "outcome" NOT NULL,
	"method" text,
	"method_detail" text,
	"round" integer,
	"time_seconds" integer,
	"knockdowns" integer,
	"sig_strikes_landed" integer,
	"sig_strikes_attempted" integer,
	"total_strikes_landed" integer,
	"total_strikes_attempted" integer,
	"takedowns_landed" integer,
	"takedowns_attempted" integer,
	"sub_attempts" integer,
	"ctrl_seconds" integer,
	"reversals" integer,
	CONSTRAINT "fight_results_fight_id_fighter_id_pk" PRIMARY KEY("fight_id","fighter_id")
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "fight_round_stats" (
	"fight_id" varchar(16) NOT NULL,
	"fighter_id" varchar(16) NOT NULL,
	"round" integer NOT NULL,
	"knockdowns" integer,
	"sig_strikes_landed" integer,
	"sig_strikes_attempted" integer,
	"total_strikes_landed" integer,
	"total_strikes_attempted" integer,
	"takedowns_landed" integer,
	"takedowns_attempted" integer,
	"sub_attempts" integer,
	"ctrl_seconds" integer,
	"reversals" integer,
	CONSTRAINT "fight_round_stats_fight_id_fighter_id_round_pk" PRIMARY KEY("fight_id","fighter_id","round")
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "fighter_backfill_state" (
	"fighter_id" varchar(16) PRIMARY KEY NOT NULL,
	"last_backfilled_at" timestamp with time zone,
	"history_count_at_backfill" integer DEFAULT 0 NOT NULL,
	"last_known_fight_id" varchar(16),
	"status" "backfill_status" DEFAULT 'none' NOT NULL,
	"last_error" text
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "fighter_stat_snapshots" (
	"fighter_id" varchar(16) NOT NULL,
	"snapshot_at" timestamp with time zone NOT NULL,
	"slpm" real,
	"str_acc" real,
	"sapm" real,
	"str_def" real,
	"td_avg" real,
	"td_acc" real,
	"td_def" real,
	"sub_avg" real,
	"wins" integer,
	"losses" integer,
	"draws" integer,
	"ufc_fight_count" integer,
	"days_since_last_fight" integer,
	"primary_weight_class" text,
	CONSTRAINT "fighter_stat_snapshots_fighter_id_snapshot_at_pk" PRIMARY KEY("fighter_id","snapshot_at")
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "fights" (
	"id" varchar(16) PRIMARY KEY NOT NULL,
	"event_id" varchar(16) NOT NULL,
	"weight_class" text,
	"scheduled_rounds" integer,
	"is_headliner" boolean DEFAULT false NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "model_versions" (
	"id" varchar(32) PRIMARY KEY NOT NULL,
	"trained_at" timestamp with time zone NOT NULL,
	"training_set_size" integer NOT NULL,
	"accuracy" real,
	"log_loss" real,
	"brier_score" real,
	"roc_auc" real,
	"model_path" text NOT NULL,
	"feature_importance" text
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "odds_snapshots" (
	"event_id" varchar(16),
	"fight_id" varchar(16),
	"fighter_id" varchar(16) NOT NULL,
	"snapshot_at" timestamp with time zone NOT NULL,
	"bookmaker" text NOT NULL,
	"decimal_odds" real NOT NULL,
	"american_odds" integer NOT NULL,
	CONSTRAINT "odds_snapshots_fighter_id_snapshot_at_bookmaker_pk" PRIMARY KEY("fighter_id","snapshot_at","bookmaker")
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "predictions" (
	"fight_id" varchar(16) NOT NULL,
	"model_version" varchar(32) NOT NULL,
	"predicted_at" timestamp with time zone NOT NULL,
	"predicted_winner_id" varchar(16) NOT NULL,
	"win_prob" real NOT NULL,
	"edge_pct" real,
	CONSTRAINT "predictions_fight_id_model_version_predicted_at_pk" PRIMARY KEY("fight_id","model_version","predicted_at")
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "fight_results" ADD CONSTRAINT "fight_results_fight_id_fights_id_fk" FOREIGN KEY ("fight_id") REFERENCES "public"."fights"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "fight_results" ADD CONSTRAINT "fight_results_fighter_id_fighters_id_fk" FOREIGN KEY ("fighter_id") REFERENCES "public"."fighters"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "fight_results" ADD CONSTRAINT "fight_results_opponent_id_fighters_id_fk" FOREIGN KEY ("opponent_id") REFERENCES "public"."fighters"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "fight_round_stats" ADD CONSTRAINT "fight_round_stats_fight_id_fights_id_fk" FOREIGN KEY ("fight_id") REFERENCES "public"."fights"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "fight_round_stats" ADD CONSTRAINT "fight_round_stats_fighter_id_fighters_id_fk" FOREIGN KEY ("fighter_id") REFERENCES "public"."fighters"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "fighter_backfill_state" ADD CONSTRAINT "fighter_backfill_state_fighter_id_fighters_id_fk" FOREIGN KEY ("fighter_id") REFERENCES "public"."fighters"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "fighter_stat_snapshots" ADD CONSTRAINT "fighter_stat_snapshots_fighter_id_fighters_id_fk" FOREIGN KEY ("fighter_id") REFERENCES "public"."fighters"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "fights" ADD CONSTRAINT "fights_event_id_events_id_fk" FOREIGN KEY ("event_id") REFERENCES "public"."events"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "odds_snapshots" ADD CONSTRAINT "odds_snapshots_event_id_events_id_fk" FOREIGN KEY ("event_id") REFERENCES "public"."events"("id") ON DELETE set null ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "odds_snapshots" ADD CONSTRAINT "odds_snapshots_fight_id_fights_id_fk" FOREIGN KEY ("fight_id") REFERENCES "public"."fights"("id") ON DELETE set null ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "odds_snapshots" ADD CONSTRAINT "odds_snapshots_fighter_id_fighters_id_fk" FOREIGN KEY ("fighter_id") REFERENCES "public"."fighters"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "predictions" ADD CONSTRAINT "predictions_fight_id_fights_id_fk" FOREIGN KEY ("fight_id") REFERENCES "public"."fights"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "predictions" ADD CONSTRAINT "predictions_model_version_model_versions_id_fk" FOREIGN KEY ("model_version") REFERENCES "public"."model_versions"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "predictions" ADD CONSTRAINT "predictions_predicted_winner_id_fighters_id_fk" FOREIGN KEY ("predicted_winner_id") REFERENCES "public"."fighters"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
