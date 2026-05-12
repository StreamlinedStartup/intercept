/**
 * Ufcstats Domain Plugin
 *
 * Provides API interception and proxy routes for ufcstats.com.
 *
 * @module domain-ufcstats
 */

import type { DomainPlugin } from '@interceptor/browser/handler/domain-loader';
import { ufcstatsInterceptorConfig } from './config';
import { UfcstatsInterceptor } from './interceptor';
import { routes } from './routes';

export const plugin: DomainPlugin = {
	domainName: 'ufcstats',
	config: ufcstatsInterceptorConfig,
	routes,

	createInterceptor: () => new UfcstatsInterceptor(),

	detectLoginPage: (url: string) => url.includes('ufcstats.com/login'),

	onVerified: (result) => ({
		type: 'ufcstats_verified',
		accountNumber: result.accountNumber,
	}),

	onVerificationFailed: (error) => ({
		type: 'ufcstats_verification_failed',
		error,
	}),

	onLoginDetected: () => ({
		type: 'ufcstats_login_page_detected',
	}),
};

export { ufcstatsInterceptorConfig } from './config';
export { UfcstatsInterceptor } from './interceptor';
export { routes } from './routes';
