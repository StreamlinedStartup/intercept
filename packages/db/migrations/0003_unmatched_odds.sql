CREATE TABLE IF NOT EXISTS "unmatched_odds" (
	"id" text PRIMARY KEY NOT NULL,
	"raw_event_name" text NOT NULL,
	"raw_fighter_a" text NOT NULL,
	"raw_fighter_b" text NOT NULL,
	"raw_date" date NOT NULL,
	"snapshot_id" text NOT NULL,
	"reason" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
