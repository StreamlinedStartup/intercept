/**
 * Odds Mma Interceptor
 *
 * Extends GenericInterceptor for the-odds-api.com API traffic capture.
 */

import { GenericInterceptor } from '@interceptor/browser/shared/interceptor';
import { oddsMmaInterceptorConfig } from './config';

export class OddsMmaInterceptor extends GenericInterceptor {
	constructor() {
		super(oddsMmaInterceptorConfig);
	}
}
