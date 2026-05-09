/**
 * Odds Mma Interceptor Configuration
 *
 * Captures API traffic from the-odds-api.com and its subdomains.
 */

import type { InterceptorConfig } from '@interceptor/browser/shared/config';

export const oddsMmaInterceptorConfig: InterceptorConfig = {
	domainName: 'odds-mma',

	interceptPatterns: [
		'https://api.the-odds-api.com/**',
		'https://the-odds-api.com/**',
		'https://www.the-odds-api.com/**',
	],

	requiredHeaders: [],
	// headerSchema is optional — omit for public APIs with no required headers.
	// For auth-gated APIs, add: headerSchema: z.object({ 'X-Api-Key': z.string() })

	baseUrls: [
		'https://api.the-odds-api.com',
		'https://the-odds-api.com',
		'https://www.the-odds-api.com',
	],
};
