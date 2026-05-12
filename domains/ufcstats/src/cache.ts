/**
 * Tiny file-based JSON cache for the ufcstats domain.
 *
 * ufcstats.com data falls into two buckets:
 *   • historical (fight detail, completed event detail): immutable once
 *     an event happens — cache effectively forever.
 *   • mutable (fighter stats, upcoming cards, listings): changes when a
 *     new fight occurs or UFC announces / shuffles a card — cache for
 *     hours to days.
 *
 * Cache files live under `data/cache/ufcstats/<bucket>/<key>.json` and
 * are JSON envelopes: `{ savedAt: <epochMs>, ttlMs: <number>, data: T }`.
 *
 * The cache is intentionally simple: synchronous fs access, no LRU eviction.
 * It's fine for the volume this domain sees (a few hundred fighters, dozens
 * of events). Stale entries are pruned passively on read.
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { DEBUG } from '@interceptor/shared';

/**
 * Resolves to <repo-root>/data/cache/ufcstats. We anchor to this file's
 * own location (`domains/ufcstats/src/cache.ts`) instead of `process.cwd()`
 * so the cache lives in a predictable spot regardless of which workspace
 * package starts the server. Honors `UFCSTATS_CACHE_DIR` for override /
 * testing.
 */
const CACHE_ROOT =
	process.env.UFCSTATS_CACHE_DIR ??
	resolve(
		fileURLToPath(new URL('.', import.meta.url)),
		'..',
		'..',
		'..',
		'data',
		'cache',
		'ufcstats',
	);

/** Per-bucket TTLs (ms). Picked from the data's actual mutation frequency. */
export const TTL = {
	/** Fighter career stats only change after they fight (every few months for active fighters). */
	fighter: 7 * 24 * 60 * 60 * 1000, // 7 days
	/** Fight detail is historical — stats never change once recorded. */
	fight: 365 * 24 * 60 * 60 * 1000, // 1 year
	/** Completed events are immutable. */
	eventCompleted: 365 * 24 * 60 * 60 * 1000, // 1 year
	/** Upcoming events can shuffle (injuries, replacements, weight changes). */
	eventUpcoming: 60 * 60 * 1000, // 1 hour
	/** Upcoming events listing — short to catch new announcements. */
	upcomingList: 30 * 60 * 1000, // 30 min
	/** Completed events listing — UFC adds events weekly. */
	completedList: 6 * 60 * 60 * 1000, // 6 hours
	/** Fighter listings (a-z) — new fighters get added but the lists are large. */
	fighterList: 24 * 60 * 60 * 1000, // 24 hours
} as const;

export type CacheBucket = keyof typeof TTL;

type Envelope<T> = {
	savedAt: number;
	ttlMs: number;
	data: T;
};

/**
 * Sanitize a cache key into a safe filename. Any non-`[a-z0-9_-]` becomes `_`.
 * Empty input is rejected — callers must not pass "" because that would
 * collide on `index.json`.
 */
function safeKey(key: string): string {
	const sanitized = key.toLowerCase().replace(/[^a-z0-9_-]+/g, '_');
	if (!sanitized) {
		throw new Error('cache key must contain at least one safe character');
	}
	return sanitized;
}

function pathFor(bucket: CacheBucket, key: string): string {
	return join(CACHE_ROOT, bucket, `${safeKey(key)}.json`);
}

/**
 * Read a cached value. Returns null on miss or expiry.
 * Corrupt / unparseable files are treated as misses.
 */
export function cacheGet<T>(bucket: CacheBucket, key: string): T | null {
	const file = pathFor(bucket, key);
	if (!existsSync(file)) return null;
	try {
		const env = JSON.parse(readFileSync(file, 'utf8')) as Envelope<T>;
		const age = Date.now() - env.savedAt;
		if (age > env.ttlMs) {
			DEBUG('ufcstats-cache', `expired bucket=${bucket} key=${key} ageMs=${age}`);
			return null;
		}
		DEBUG('ufcstats-cache', `hit bucket=${bucket} key=${key} ageMs=${age}`);
		return env.data;
	} catch (err) {
		DEBUG(
			'ufcstats-cache',
			`read-failed bucket=${bucket} key=${key} err=${err instanceof Error ? err.message : 'unknown'}`,
		);
		return null;
	}
}

/**
 * Persist a value under a cache key with the bucket's default TTL.
 * Failures are logged but never thrown — caching is best-effort.
 */
export function cacheSet<T>(bucket: CacheBucket, key: string, data: T): void {
	const file = pathFor(bucket, key);
	const env: Envelope<T> = { savedAt: Date.now(), ttlMs: TTL[bucket], data };
	try {
		mkdirSync(dirname(file), { recursive: true });
		writeFileSync(file, JSON.stringify(env), 'utf8');
		DEBUG('ufcstats-cache', `wrote bucket=${bucket} key=${key}`);
	} catch (err) {
		DEBUG(
			'ufcstats-cache',
			`write-failed bucket=${bucket} key=${key} err=${err instanceof Error ? err.message : 'unknown'}`,
		);
	}
}

/**
 * Build the `Cache-Control` header value for a bucket's TTL. Browsers and
 * upstream proxies see the same lifetime as the disk cache.
 */
export function cacheControlHeader(bucket: CacheBucket): string {
	const seconds = Math.floor(TTL[bucket] / 1000);
	return `public, max-age=${seconds}`;
}
