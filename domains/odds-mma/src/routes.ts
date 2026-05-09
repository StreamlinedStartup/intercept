import type { DomainRoute } from '@interceptor/browser/handler/domain-loader';
import { DEBUG, rateLimitedFetch } from '@interceptor/shared';
import { cacheControlHeader, cacheGet, cacheSet } from './cache';

type RouteCtx = {
	req: { url: string };
	header: (k: string, v: string) => void;
	json: (body: unknown, status?: number) => Response;
};

const ODDS_API_BASE_URL = 'https://api.the-odds-api.com/v4';
const MMA_SPORT_KEY = 'mma_mixed_martial_arts';
const UPCOMING_CACHE_KEY = 'mma_mixed_martial_arts-us-h2h';

function parseJsonOrText(text: string): unknown {
	try {
		return JSON.parse(text) as unknown;
	} catch {
		return { error: text };
	}
}

async function fetchUpcomingOdds(): Promise<{
	body: unknown;
	status: number;
	requestsRemaining: string | null;
}> {
	const apiKey = process.env.ODDS_API_KEY;
	if (!apiKey) {
		return {
			body: { error: 'ODDS_API_KEY is required for /api/odds-mma/upcoming' },
			status: 500,
			requestsRemaining: null,
		};
	}

	const url = new URL(`${ODDS_API_BASE_URL}/sports/${MMA_SPORT_KEY}/odds`);
	url.searchParams.set('regions', 'us');
	url.searchParams.set('markets', 'h2h');
	url.searchParams.set('apiKey', apiKey);

	const res = await rateLimitedFetch(url, {
		headers: { Accept: 'application/json' },
	});
	const requestsRemaining = res.headers.get('x-requests-remaining');
	if (requestsRemaining) {
		DEBUG('odds-mma', `x-requests-remaining=${requestsRemaining}`);
	}

	const body = parseJsonOrText(await res.text());
	return {
		body,
		status: res.ok ? 200 : res.status,
		requestsRemaining,
	};
}

async function cachedUpcoming(c: RouteCtx): Promise<Response> {
	const url = new URL(c.req.url);
	const bypass = url.searchParams.get('refresh') === '1' || url.searchParams.get('nocache') === '1';

	if (!bypass) {
		const hit = cacheGet<unknown>('oddsList', UPCOMING_CACHE_KEY);
		if (hit) {
			c.header('X-Cache', 'HIT');
			c.header('Cache-Control', cacheControlHeader('oddsList'));
			return c.json(hit);
		}
	}

	const result = await fetchUpcomingOdds();
	if (result.requestsRemaining) {
		c.header('X-Odds-Requests-Remaining', result.requestsRemaining);
	}

	if (result.status >= 200 && result.status < 300) {
		cacheSet('oddsList', UPCOMING_CACHE_KEY, result.body);
		c.header('X-Cache', bypass ? 'BYPASS' : 'MISS');
		c.header('Cache-Control', cacheControlHeader('oddsList'));
		return c.json(result.body);
	}

	c.header('X-Cache', 'SKIP');
	return c.json(result.body, result.status);
}

export const routes: DomainRoute[] = [
	{
		method: 'GET',
		path: '/upcoming',
		description: 'Current UFC/MMA moneyline odds from the-odds-api.',
		browserRequired: false,
		handler: cachedUpcoming,
	},
];
