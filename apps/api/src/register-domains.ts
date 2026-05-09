/**
 * Domain Registration & Rate Limits
 *
 * Imports and registers all domain plugins at application startup.
 * Also registers outbound rate limits for known external APIs.
 *
 * The browser handler uses getDomain() to look up plugins by name —
 * it has zero knowledge of which domains are registered.
 *
 * @module api/register-domains
 */

import { registerDomain } from '@interceptor/browser/handler/domain-loader';
import { plugin as boardshop } from '@interceptor/domain-boardshop';
import { plugin as oddsMma } from '@interceptor/domain-odds-mma';
import { plugin as ufcstats } from '@interceptor/domain-ufcstats';
import { registerRateLimit } from '@interceptor/shared';

// ─── Domain plugins ──────────────────────────────────────────────────

registerDomain(boardshop);
registerDomain(oddsMma);
registerDomain(ufcstats);

// ─── Outbound rate limits (per-hostname) ─────────────────────────────

registerRateLimit('api.boardshop.example.com', { maxPerMinute: 30, retryOn429: 2 });
registerRateLimit('api.the-odds-api.com', { maxPerMinute: 5, retryOn429: 2 });
// ufcstats.com — be a polite citizen on a small public stats site.
registerRateLimit('ufcstats.com', { maxPerMinute: 30, retryOn429: 2 });
