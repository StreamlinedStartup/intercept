CREATE TYPE "public"."promotion" AS ENUM('ufc', 'bellator', 'strikeforce', 'other');--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "events" (
	"id" varchar(16) PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"date" date NOT NULL,
	"location" text,
	"completed" boolean DEFAULT false NOT NULL,
	"promotion" "promotion" DEFAULT 'ufc' NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "fighters" (
	"id" varchar(16) PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"nickname" text,
	"dob" date,
	"height_in" real,
	"reach_in" real,
	"stance" text,
	"history_count" integer DEFAULT 0 NOT NULL
);
