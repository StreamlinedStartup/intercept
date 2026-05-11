CREATE TABLE IF NOT EXISTS "historical_odds_import_runs" (
	"id" text PRIMARY KEY NOT NULL,
	"source" text NOT NULL,
	"source_url" text NOT NULL,
	"source_event_id" text NOT NULL,
	"started_at" timestamp with time zone NOT NULL,
	"finished_at" timestamp with time zone,
	"status" text NOT NULL,
	"events_read" integer DEFAULT 0 NOT NULL,
	"fights_read" integer DEFAULT 0 NOT NULL,
	"moneylines_read" integer DEFAULT 0 NOT NULL,
	"matched_rows" integer DEFAULT 0 NOT NULL,
	"unmatched_rows" integer DEFAULT 0 NOT NULL,
	"raw_metadata" text NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "historical_odds_events" (
	"id" text PRIMARY KEY NOT NULL,
	"source" text NOT NULL,
	"source_event_id" text NOT NULL,
	"source_event_global_id" text,
	"source_slug" text NOT NULL,
	"source_url" text NOT NULL,
	"raw_name" text NOT NULL,
	"event_date" date NOT NULL,
	"venue" text,
	"city" text,
	"promotion" text NOT NULL,
	"canonical_event_id" text,
	"match_status" text NOT NULL,
	"match_reason" text NOT NULL,
	"raw_metadata" text NOT NULL,
	"scraped_at" timestamp with time zone NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "historical_odds_events_source_event_idx" UNIQUE("source","source_event_id")
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "historical_odds_fights" (
	"id" text PRIMARY KEY NOT NULL,
	"historical_event_id" text NOT NULL,
	"source_fight_id" text NOT NULL,
	"source_fight_slug" text NOT NULL,
	"source_url" text NOT NULL,
	"raw_fighter_a" text NOT NULL,
	"raw_fighter_b" text NOT NULL,
	"source_fighter_a_id" text NOT NULL,
	"source_fighter_b_id" text NOT NULL,
	"source_fighter_a_slug" text NOT NULL,
	"source_fighter_b_slug" text NOT NULL,
	"is_cancelled" boolean DEFAULT false NOT NULL,
	"prop_count" integer DEFAULT 0 NOT NULL,
	"best_odds_a" integer,
	"best_odds_b" integer,
	"canonical_fight_id" text,
	"canonical_fighter_a_id" text,
	"canonical_fighter_b_id" text,
	"match_status" text NOT NULL,
	"match_reason" text NOT NULL,
	"candidate_matches" text NOT NULL,
	"raw_metadata" text NOT NULL,
	"scraped_at" timestamp with time zone NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "historical_odds_fights_source_fight_idx" UNIQUE("historical_event_id","source_fight_id")
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "historical_moneyline_odds" (
	"id" text PRIMARY KEY NOT NULL,
	"import_run_id" text NOT NULL,
	"historical_fight_id" text NOT NULL,
	"source_offer_id" text NOT NULL,
	"sportsbook_id" text NOT NULL,
	"sportsbook_slug" text NOT NULL,
	"sportsbook_name" text NOT NULL,
	"source_outcome_id" text NOT NULL,
	"raw_fighter_name" text NOT NULL,
	"source_fighter_id" text NOT NULL,
	"canonical_fighter_id" text,
	"side" text NOT NULL,
	"line_kind" text NOT NULL,
	"american_odds" integer NOT NULL,
	"decimal_odds" real NOT NULL,
	"implied_probability" real NOT NULL,
	"market_timestamp" timestamp with time zone,
	"market_timestamp_semantics" text NOT NULL,
	"scraped_at" timestamp with time zone NOT NULL,
	"raw_metadata" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "historical_moneyline_odds_source_outcome_idx" UNIQUE("import_run_id","source_offer_id","source_outcome_id","line_kind")
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "unmatched_historical_odds" (
	"id" text PRIMARY KEY NOT NULL,
	"source" text NOT NULL,
	"source_event_id" text NOT NULL,
	"source_fight_id" text NOT NULL,
	"source_url" text NOT NULL,
	"raw_event_name" text NOT NULL,
	"raw_event_date" date NOT NULL,
	"raw_fighter_a" text NOT NULL,
	"raw_fighter_b" text NOT NULL,
	"raw_sportsbook" text,
	"raw_odds" text NOT NULL,
	"candidate_matches" text NOT NULL,
	"reason" text NOT NULL,
	"reviewed" boolean DEFAULT false NOT NULL,
	"reviewed_at" timestamp with time zone,
	"review_note" text,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_odds_events" ADD CONSTRAINT "hist_odds_events_canonical_event_fk" FOREIGN KEY ("canonical_event_id") REFERENCES "public"."events"("id") ON DELETE set null ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_odds_fights" ADD CONSTRAINT "hist_odds_fights_event_fk" FOREIGN KEY ("historical_event_id") REFERENCES "public"."historical_odds_events"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_odds_fights" ADD CONSTRAINT "hist_odds_fights_canonical_fight_fk" FOREIGN KEY ("canonical_fight_id") REFERENCES "public"."fights"("id") ON DELETE set null ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_odds_fights" ADD CONSTRAINT "hist_odds_fights_canonical_fighter_a_fk" FOREIGN KEY ("canonical_fighter_a_id") REFERENCES "public"."fighters"("id") ON DELETE set null ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_odds_fights" ADD CONSTRAINT "hist_odds_fights_canonical_fighter_b_fk" FOREIGN KEY ("canonical_fighter_b_id") REFERENCES "public"."fighters"("id") ON DELETE set null ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_moneyline_odds" ADD CONSTRAINT "hist_moneylines_import_run_fk" FOREIGN KEY ("import_run_id") REFERENCES "public"."historical_odds_import_runs"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_moneyline_odds" ADD CONSTRAINT "hist_moneylines_fight_fk" FOREIGN KEY ("historical_fight_id") REFERENCES "public"."historical_odds_fights"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_moneyline_odds" ADD CONSTRAINT "hist_moneylines_canonical_fighter_fk" FOREIGN KEY ("canonical_fighter_id") REFERENCES "public"."fighters"("id") ON DELETE set null ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
