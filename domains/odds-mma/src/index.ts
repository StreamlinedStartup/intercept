/**
 * Odds Mma Domain Plugin
 *
 * Provides API interception and proxy routes for the-odds-api.com.
 *
 * @module domain-odds-mma
 */

import type { DomainPlugin } from '@interceptor/browser/handler/domain-loader';
import { oddsMmaInterceptorConfig } from './config';
import { OddsMmaInterceptor } from './interceptor';
import { routes } from './routes';

export const plugin: DomainPlugin = {
	domainName: 'odds-mma',
	config: oddsMmaInterceptorConfig,
	routes,

	createInterceptor: () => new OddsMmaInterceptor(),

	detectLoginPage: (url: string) => url.includes('the-odds-api.com/login'),

	onVerified: (result) => ({
		type: 'odds-mma_verified',
		accountNumber: result.accountNumber,
	}),

	onVerificationFailed: (error) => ({
		type: 'odds-mma_verification_failed',
		error,
	}),

	onLoginDetected: () => ({
		type: 'odds-mma_login_page_detected',
	}),
};

export { oddsMmaInterceptorConfig } from './config';
export { OddsMmaInterceptor } from './interceptor';
export { routes } from './routes';
