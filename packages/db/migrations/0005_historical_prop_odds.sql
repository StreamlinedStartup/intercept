CREATE TABLE IF NOT EXISTS "historical_prop_odds" (
	"id" text PRIMARY KEY NOT NULL,
	"import_run_id" text NOT NULL,
	"historical_fight_id" text NOT NULL,
	"source_event_id" text NOT NULL,
	"source_fight_id" text NOT NULL,
	"source_market_id" text NOT NULL,
	"source_offer_id" text NOT NULL,
	"source_offer_type_id" text NOT NULL,
	"market_family" text NOT NULL,
	"market_label" text NOT NULL,
	"prop_name" text NOT NULL,
	"sportsbook_id" text NOT NULL,
	"sportsbook_slug" text NOT NULL,
	"sportsbook_name" text NOT NULL,
	"source_outcome_id" text NOT NULL,
	"raw_outcome_name" text NOT NULL,
	"raw_fighter_name" text,
	"source_fighter_id" text,
	"canonical_fighter_id" text,
	"side" text NOT NULL,
	"outcome_side" text NOT NULL,
	"is_not" boolean DEFAULT false NOT NULL,
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
	CONSTRAINT "historical_prop_odds_source_outcome_idx" UNIQUE("import_run_id","source_market_id","source_offer_id","source_outcome_id","line_kind")
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_prop_odds" ADD CONSTRAINT "hist_prop_odds_import_run_fk" FOREIGN KEY ("import_run_id") REFERENCES "public"."historical_odds_import_runs"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_prop_odds" ADD CONSTRAINT "hist_prop_odds_fight_fk" FOREIGN KEY ("historical_fight_id") REFERENCES "public"."historical_odds_fights"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "historical_prop_odds" ADD CONSTRAINT "hist_prop_odds_canonical_fighter_fk" FOREIGN KEY ("canonical_fighter_id") REFERENCES "public"."fighters"("id") ON DELETE set null ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
