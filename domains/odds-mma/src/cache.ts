/**
 * Tiny file-based JSON cache for the odds-mma domain.
 *
 * Cache files live under `data/cache/odds-mma/<bucket>/<key>.json` and
 * are JSON envelopes: `{ savedAt: <epochMs>, ttlMs: <number>, data: T }`.
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { DEBUG } from '@interceptor/shared';

const CACHE_ROOT =
	process.env.ODDS_MMA_CACHE_DIR ??
	resolve(
		fileURLToPath(new URL('.', import.meta.url)),
		'..',
		'..',
		'..',
		'data',
		'cache',
		'odds-mma',
	);

export const TTL = {
	oddsList: 60 * 60 * 1000,
	oddsHistorical: 365 * 24 * 60 * 60 * 1000,
} as const;

export type CacheBucket = keyof typeof TTL;

type Envelope<T> = {
	savedAt: number;
	ttlMs: number;
	data: T;
};

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

export function cacheGet<T>(bucket: CacheBucket, key: string): T | null {
	const file = pathFor(bucket, key);
	if (!existsSync(file)) return null;
	try {
		const env = JSON.parse(readFileSync(file, 'utf8')) as Envelope<T>;
		const age = Date.now() - env.savedAt;
		if (age > env.ttlMs) {
			DEBUG('odds-mma-cache', `expired bucket=${bucket} key=${key} ageMs=${age}`);
			return null;
		}
		DEBUG('odds-mma-cache', `hit bucket=${bucket} key=${key} ageMs=${age}`);
		return env.data;
	} catch (err) {
		DEBUG(
			'odds-mma-cache',
			`read-failed bucket=${bucket} key=${key} err=${err instanceof Error ? err.message : 'unknown'}`,
		);
		return null;
	}
}

export function cacheSet<T>(bucket: CacheBucket, key: string, data: T): void {
	const file = pathFor(bucket, key);
	const env: Envelope<T> = { savedAt: Date.now(), ttlMs: TTL[bucket], data };
	try {
		mkdirSync(dirname(file), { recursive: true });
		writeFileSync(file, JSON.stringify(env), 'utf8');
		DEBUG('odds-mma-cache', `wrote bucket=${bucket} key=${key}`);
	} catch (err) {
		DEBUG(
			'odds-mma-cache',
			`write-failed bucket=${bucket} key=${key} err=${err instanceof Error ? err.message : 'unknown'}`,
		);
	}
}

export function cacheControlHeader(bucket: CacheBucket): string {
	const seconds = Math.floor(TTL[bucket] / 1000);
	return `public, max-age=${seconds}`;
}
