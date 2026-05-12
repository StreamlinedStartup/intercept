/**
 * Ufcstats Interceptor
 *
 * Extends GenericInterceptor for ufcstats.com API traffic capture.
 */

import { GenericInterceptor } from '@interceptor/browser/shared/interceptor';
import { ufcstatsInterceptorConfig } from './config';

export class UfcstatsInterceptor extends GenericInterceptor {
	constructor() {
		super(ufcstatsInterceptorConfig);
	}
}
