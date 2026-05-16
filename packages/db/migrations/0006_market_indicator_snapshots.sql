CREATE TABLE IF NOT EXISTS "market_indicator_snapshots" (
	"fight_id" text NOT NULL,
	"target" text NOT NULL,
	"model_version" text NOT NULL,
	"indicator_name" text NOT NULL,
	"computed_at" timestamp with time zone NOT NULL,
	"model_probability" real NOT NULL,
	"market_probability" real,
	"edge_pct" real,
	"candidate" boolean DEFAULT false NOT NULL,
	"market_pair_count" integer DEFAULT 0 NOT NULL,
	"value_status" text DEFAULT 'research_only' NOT NULL,
	"source_report" text NOT NULL,
	"source_config" text,
	"source_git_sha" text,
	"source_model_path" text,
	"source_data_window" text,
	"staleness_reason" text,
	"raw_metadata" text DEFAULT '{}' NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "market_indicator_snapshots_pk" PRIMARY KEY("fight_id","target","model_version","indicator_name")
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "market_indicator_snapshots" ADD CONSTRAINT "market_indicator_snapshots_fight_fk" FOREIGN KEY ("fight_id") REFERENCES "public"."fights"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS "market_indicator_snapshots_fight_target_computed_at_idx" ON "market_indicator_snapshots" ("fight_id","target","computed_at");
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS "market_indicator_snapshots_value_status_computed_at_idx" ON "market_indicator_snapshots" ("value_status","computed_at");
