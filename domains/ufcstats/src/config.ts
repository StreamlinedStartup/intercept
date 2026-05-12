/**
 * UFC Stats Interceptor Configuration
 *
 * Captures traffic from ufcstats.com — the official UFC fight statistics site.
 *
 * Note: ufcstats.com is fully server-rendered classic HTML. There are no XHR
 * data endpoints. All routes parse HTML with cheerio. The interceptor exists
 * for symmetry with the plugin contract, but no JSON traffic is expected to
 * be captured.
 */

import type { InterceptorConfig } from '@interceptor/browser/shared/config';

export const ufcstatsInterceptorConfig: InterceptorConfig = {
	domainName: 'ufcstats',

	interceptPatterns: ['http://ufcstats.com/**', 'https://ufcstats.com/**'],

	requiredHeaders: [],

	baseUrls: ['http://ufcstats.com'],
};
