/**
 * UFC Stats API Routes
 *
 * ufcstats.com is fully server-rendered classic HTML (jQuery 1.10 stack, no SPA,
 * no JSON XHR endpoints). The site IS the API — every route below fetches an
 * HTML page and parses it with cheerio. Direct rateLimitedFetch works without
 * any auth, cookies, or special headers (Gap=N for every endpoint).
 *
 * Pagination is purely URL-based:
 *   /statistics/fighters?char=<a-z>&page=all   — fighter listing by letter
 *   /statistics/events/completed?page=N|all    — completed events listing
 *   /statistics/events/upcoming                — upcoming events (single page)
 *   /fighter-details/<id>                      — single fighter (full history)
 *   /event-details/<id>                        — single event (fight card)
 *   /fight-details/<id>                        — single fight (round-by-round)
 *
 * IDs are 16-char hex strings.
 *
 * @module domain-ufcstats/routes
 */

import type { DomainRoute } from '@interceptor/browser/handler/domain-loader';
import { DEBUG, rateLimitedFetch } from '@interceptor/shared';
import { type CacheBucket, cacheControlHeader, cacheGet, cacheSet } from './cache';

/**
 * Minimal subset of Hono's Context that `cachedJson` needs. Inlined to avoid
 * a hard dep on `hono` from the domain package — handlers receive the same
 * Context shape from the API server.
 */
type RouteCtx = {
	req: { url: string };
	header: (k: string, v: string) => void;
	json: (body: Record<string, unknown> | unknown, status?: number) => Response;
};

type CheerioAPI = Awaited<ReturnType<typeof import('cheerio').load>>;
type CheerioElement = ReturnType<CheerioAPI>[number];

const BASE_URL = process.env.UFCSTATS_URL ?? 'http://ufcstats.com';
const ID_RE = /^[a-f0-9]{16}$/;

function clean(s: string | null | undefined): string {
	return (s ?? '').replace(/\s+/g, ' ').trim();
}

function notFoundIfEmptyId(id: string): string | null {
	return ID_RE.test(id) ? null : 'Invalid id (expected 16-char hex)';
}

async function fetchHtml(url: string): Promise<{ ok: boolean; html: string; status: number }> {
	DEBUG('ufcstats', `fetching ${url}`);
	const res = await rateLimitedFetch(url);
	const html = await res.text();
	return { ok: res.ok, html, status: res.status };
}

async function loadCheerio(html: string): Promise<CheerioAPI> {
	const { load } = await import('cheerio');
	return load(html);
}

/**
 * Wrap a handler's data-producing logic with disk caching.
 *
 * Behavior:
 *   • `?refresh=1` (or `?nocache=1`) bypasses the cache lookup but still
 *     stores the fresh response — useful for "force update".
 *   • Cache hits set `X-Cache: HIT` and reuse the bucket's `Cache-Control`
 *     so browsers/proxies cache to the same lifetime.
 *   • Misses fetch+parse via `produce`, store, then return with `X-Cache: MISS`.
 *
 * The producer returns `{ data, status }` where status is the response code
 * (e.g. 502 on upstream failure) and data is the JSON body. Non-2xx
 * responses are NOT cached.
 */
async function cachedJson<T>(
	c: RouteCtx,
	bucket: CacheBucket,
	key: string,
	produce: () => Promise<{ data: T; status: number } | { error: unknown; status: number }>,
): Promise<Response> {
	const url = new URL(c.req.url);
	const bypass = url.searchParams.get('refresh') === '1' || url.searchParams.get('nocache') === '1';

	if (!bypass) {
		const hit = cacheGet<T>(bucket, key);
		if (hit) {
			c.header('X-Cache', 'HIT');
			c.header('Cache-Control', cacheControlHeader(bucket));
			return c.json(hit);
		}
	}

	const result = await produce();
	if (result.status >= 200 && result.status < 300 && 'data' in result) {
		cacheSet(bucket, key, result.data);
		c.header('X-Cache', bypass ? 'BYPASS' : 'MISS');
		c.header('Cache-Control', cacheControlHeader(bucket));
		return c.json(result.data);
	}

	c.header('X-Cache', 'SKIP');
	return c.json('error' in result ? result.error : (result as { data: T }).data, result.status);
}

/**
 * Parse a fighter listing row from /statistics/fighters?char=X&page=all.
 * Columns: First, Last, Nickname, Ht., Wt., Reach, Stance, W, L, D, Belt
 */
function parseFighterListingRow($: CheerioAPI, row: CheerioElement) {
	const cells = $(row).find('td.b-statistics__table-col');
	const linkEl = cells.eq(0).find('a').first();
	const href = linkEl.attr('href') ?? '';
	const id = href.match(/fighter-details\/([a-f0-9]{16})/)?.[1] ?? null;
	return {
		id,
		first: clean(cells.eq(0).text()),
		last: clean(cells.eq(1).text()),
		nickname: clean(cells.eq(2).text()) || null,
		height: clean(cells.eq(3).text()) || null,
		weight: clean(cells.eq(4).text()) || null,
		reach: clean(cells.eq(5).text()) || null,
		stance: clean(cells.eq(6).text()) || null,
		wins: Number(clean(cells.eq(7).text())) || 0,
		losses: Number(clean(cells.eq(8).text())) || 0,
		draws: Number(clean(cells.eq(9).text())) || 0,
		belt: cells.eq(10).find('img').length > 0,
		url: href || null,
	};
}

export const routes: DomainRoute[] = [
	// ─── Route 1: Fighter listing by letter ─────────────────────────
	// /api/ufcstats/fighters/:char?page=all|N
	// :char is a single letter a-z. page=all returns every fighter for that letter.
	{
		method: 'GET',
		path: '/fighters/:char',
		description: 'List fighters by last-name letter (a-z). Optional ?page=all|N (default all).',
		browserRequired: false,
		handler: async (c) => {
			const params = c.req.param() as Record<string, string>;
			const char = (params.char ?? '').toLowerCase();
			if (!/^[a-z]$/.test(char)) {
				return c.json({ error: 'char must be a single a-z letter' }, 400);
			}
			const page = new URL(c.req.url).searchParams.get('page') ?? 'all';
			const url = `${BASE_URL}/statistics/fighters?char=${char}&page=${encodeURIComponent(page)}`;

			return cachedJson(c, 'fighterList', `${char}-${page}`, async () => {
				const { ok, html, status } = await fetchHtml(url);
				if (!ok) {
					return { error: { error: `Listing returned ${status}` }, status: 502 };
				}
				const $ = await loadCheerio(html);

				const rows = $('tr.b-statistics__table-row')
					.toArray()
					.filter((r) => $(r).find('td.b-statistics__table-col').length > 0);
				const fighters = rows.map((r) => parseFighterListingRow($, r));

				return { data: { char, page, count: fighters.length, fighters }, status: 200 };
			});
		},
	},

	// ─── Route 2: Fighter detail ─────────────────────────────────────
	// /api/ufcstats/fighter/:id  — 16-char hex id
	{
		method: 'GET',
		path: '/fighter/:id',
		description: 'Fighter profile (info + career stats + full fight history).',
		browserRequired: false,
		handler: async (c) => {
			const id = (c.req.param() as Record<string, string>).id;
			const err = notFoundIfEmptyId(id);
			if (err) return c.json({ error: err }, 400);

			return cachedJson(c, 'fighter', id, async () => {
				const { ok, html, status } = await fetchHtml(`${BASE_URL}/fighter-details/${id}`);
				if (!ok) return { error: { error: `Fighter page returned ${status}` }, status: 502 };
				const $ = await loadCheerio(html);

				const titleText = clean($('span.b-content__title-highlight').first().text());
				const recordText = clean($('span.b-content__title-record').first().text());
				const nickname =
					clean($('p.b-content__Nickname').text()).replace(/^Nickname:\s*/i, '') || null;

				// Info box: each <li> has label and value separated. Use raw text.
				const info: Record<string, string> = {};
				$('ul.b-list__box-list li.b-list__box-list-item').each((_, li) => {
					const txt = clean($(li).text());
					const m = txt.match(/^([^:]+):\s*(.*)$/);
					if (m) {
						const key = m[1]
							.trim()
							.toLowerCase()
							.replace(/[^a-z0-9]+/g, '_')
							.replace(/_+|_$/g, '_')
							.replace(/^_|_$/g, '');
						info[key] = m[2].trim();
					}
				});

				// Fight history: tbody rows with class b-fight-details__table-row.
				const history = $('tbody.b-fight-details__table-body tr.b-fight-details__table-row')
					.toArray()
					.map((row) => {
						const $row = $(row);
						const fightLink = $row.attr('data-link') ?? null;
						const fightId = fightLink?.match(/fight-details\/([a-f0-9]{16})/)?.[1] ?? null;
						const tds = $row.find('td.b-fight-details__table-col');

						// Result text comes from the flag element
						const result = clean($row.find('i.b-flag__text').text()).toLowerCase() || null;

						// Fighter cell — two <p> rows for opponent + self
						const fighterPs = tds.eq(1).find('p.b-fight-details__table-text');
						const fighters = fighterPs
							.toArray()
							.map((p) => {
								const a = $(p).find('a');
								const href = a.attr('href') ?? '';
								return {
									name: clean(a.text() || $(p).text()),
									id: href.match(/fighter-details\/([a-f0-9]{16})/)?.[1] ?? null,
								};
							})
							.filter((f) => f.name.length > 0);

						// Stat columns each have two <p> — values for fighter A and B
						const pairFromCol = (i: number): [string, string] => {
							const ps = tds.eq(i).find('p.b-fight-details__table-text');
							return [clean(ps.eq(0).text()), clean(ps.eq(1).text())];
						};

						const [kdSelf, kdOpp] = pairFromCol(2);
						const [strSelf, strOpp] = pairFromCol(3);
						const [tdSelf, tdOpp] = pairFromCol(4);
						const [subSelf, subOpp] = pairFromCol(5);

						// Event cell — link + date
						const eventTd = tds.eq(6);
						const eventA = eventTd.find('a').first();
						const eventHref = eventA.attr('href') ?? '';
						const event = {
							name: clean(eventA.text()),
							id: eventHref.match(/event-details\/([a-f0-9]{16})/)?.[1] ?? null,
							date: clean(eventTd.find('p.b-fight-details__table-text').eq(1).text()),
						};

						// Method — first <p> is method, second is detail
						const methodPs = tds.eq(7).find('p.b-fight-details__table-text');
						const method = clean(methodPs.eq(0).text());
						const methodDetail = clean(methodPs.eq(1).text()) || null;

						const round = clean(tds.eq(8).text());
						const time = clean(tds.eq(9).text());

						return {
							fightId,
							fightUrl: fightLink,
							result,
							fighters,
							stats: {
								knockdowns: { self: kdSelf, opp: kdOpp },
								strikes: { self: strSelf, opp: strOpp },
								takedowns: { self: tdSelf, opp: tdOpp },
								submissions: { self: subSelf, opp: subOpp },
							},
							event,
							method,
							methodDetail,
							round,
							time,
						};
					});

				return {
					data: {
						id,
						name: titleText,
						nickname,
						record: recordText,
						info,
						history,
						historyCount: history.length,
						url: `${BASE_URL}/fighter-details/${id}`,
					},
					status: 200,
				};
			});
		},
	},

	// ─── Route 3: Completed events listing ──────────────────────────
	// /api/ufcstats/events/completed?page=all|N
	{
		method: 'GET',
		path: '/events/completed',
		description: 'List completed UFC events. Optional ?page=all|N (default all, ~770 events).',
		browserRequired: false,
		handler: async (c) => {
			const page = new URL(c.req.url).searchParams.get('page') ?? 'all';
			const url = `${BASE_URL}/statistics/events/completed?page=${encodeURIComponent(page)}`;

			return cachedJson(c, 'completedList', `page-${page}`, async () => {
				const { ok, html, status } = await fetchHtml(url);
				if (!ok) return { error: { error: `Events page returned ${status}` }, status: 502 };
				const $ = await loadCheerio(html);

				const events = $('tr.b-statistics__table-row')
					.toArray()
					.map((row) => {
						const cells = $(row).find('td.b-statistics__table-col');
						if (cells.length === 0) return null;
						const link = cells.eq(0).find('a').first();
						const href = link.attr('href') ?? '';
						const id = href.match(/event-details\/([a-f0-9]{16})/)?.[1] ?? null;
						if (!id) return null;
						const date = clean(cells.eq(0).find('span').text());
						const name = clean(link.text());
						const location = clean(cells.eq(1).text());
						return { id, name, date, location, url: href };
					})
					.filter((e): e is NonNullable<typeof e> => e !== null);

				return { data: { page, count: events.length, events }, status: 200 };
			});
		},
	},

	// ─── Route 4: Upcoming events listing ───────────────────────────
	{
		method: 'GET',
		path: '/events/upcoming',
		description: 'List upcoming UFC events.',
		browserRequired: false,
		handler: async (c) => {
			const url = `${BASE_URL}/statistics/events/upcoming`;
			return cachedJson(c, 'upcomingList', 'all', async () => {
				const { ok, html, status } = await fetchHtml(url);
				if (!ok) return { error: { error: `Upcoming page returned ${status}` }, status: 502 };
				const $ = await loadCheerio(html);

				const events = $('tr.b-statistics__table-row')
					.toArray()
					.map((row) => {
						const cells = $(row).find('td.b-statistics__table-col');
						if (cells.length === 0) return null;
						const link = cells.eq(0).find('a').first();
						const href = link.attr('href') ?? '';
						const id = href.match(/event-details\/([a-f0-9]{16})/)?.[1] ?? null;
						if (!id) return null;
						return {
							id,
							name: clean(link.text()),
							date: clean(cells.eq(0).find('span').text()),
							location: clean(cells.eq(1).text()),
							url: href,
						};
					})
					.filter((e): e is NonNullable<typeof e> => e !== null);

				return { data: { count: events.length, events }, status: 200 };
			});
		},
	},

	// ─── Route 5: Event detail (fight card) ─────────────────────────
	// /api/ufcstats/event/:id
	{
		method: 'GET',
		path: '/event/:id',
		description: 'Event detail: header info + fight card (each fight links to /fight/:id).',
		browserRequired: false,
		handler: async (c) => {
			const id = (c.req.param() as Record<string, string>).id;
			const err = notFoundIfEmptyId(id);
			if (err) return c.json({ error: err }, 400);

			// Pick bucket dynamically from the parsed result: completed events
			// are immutable (year-long cache), upcoming cards can shuffle (hour).
			// Try the long-lived bucket first; on miss, the short-lived bucket.
			const url = new URL(c.req.url);
			const bypass =
				url.searchParams.get('refresh') === '1' || url.searchParams.get('nocache') === '1';
			if (!bypass) {
				const completedHit = cacheGet<Record<string, unknown>>('eventCompleted', id);
				if (completedHit) {
					c.header('X-Cache', 'HIT');
					c.header('Cache-Control', cacheControlHeader('eventCompleted'));
					return c.json(completedHit);
				}
				const upcomingHit = cacheGet<Record<string, unknown>>('eventUpcoming', id);
				if (upcomingHit) {
					c.header('X-Cache', 'HIT');
					c.header('Cache-Control', cacheControlHeader('eventUpcoming'));
					return c.json(upcomingHit);
				}
			}

			const { ok, html, status } = await fetchHtml(`${BASE_URL}/event-details/${id}`);
			if (!ok) return c.json({ error: `Event page returned ${status}` }, 502);
			const $ = await loadCheerio(html);

			const name = clean($('span.b-content__title-highlight').first().text());

			// Header info-box: Date, Location, Attendance
			const info: Record<string, string> = {};
			$('ul.b-list__box-list li.b-list__box-list-item').each((_, li) => {
				const txt = clean($(li).text());
				const m = txt.match(/^([^:]+):\s*(.*)$/);
				if (m) {
					const key = m[1]
						.trim()
						.toLowerCase()
						.replace(/[^a-z0-9]+/g, '_');
					info[key] = m[2].trim();
				}
			});

			// Fight card rows
			const fights = $('tbody.b-fight-details__table-body tr.b-fight-details__table-row')
				.toArray()
				.map((row) => {
					const $row = $(row);
					const fightLink = $row.attr('data-link') ?? null;
					const fightId = fightLink?.match(/fight-details\/([a-f0-9]{16})/)?.[1] ?? null;
					const tds = $row.find('td.b-fight-details__table-col');

					const result = clean(tds.eq(0).find('i.b-flag__text').text()).toLowerCase() || null;

					const fighterAs = tds.eq(1).find('a.b-link');
					const fighters = fighterAs
						.toArray()
						.map((a) => {
							const href = $(a).attr('href') ?? '';
							return {
								name: clean($(a).text()),
								id: href.match(/fighter-details\/([a-f0-9]{16})/)?.[1] ?? null,
							};
						})
						.filter((f) => f.name);

					const pairFromCol = (i: number): [string, string] => {
						const ps = tds.eq(i).find('p.b-fight-details__table-text');
						return [clean(ps.eq(0).text()), clean(ps.eq(1).text())];
					};
					const [kd1, kd2] = pairFromCol(2);
					const [str1, str2] = pairFromCol(3);
					const [td1, td2] = pairFromCol(4);
					const [sub1, sub2] = pairFromCol(5);

					const weightClass = clean(tds.eq(6).text());
					const methodPs = tds.eq(7).find('p.b-fight-details__table-text');
					const method = clean(methodPs.eq(0).text());
					const methodDetail = clean(methodPs.eq(1).text()) || null;
					const round = clean(tds.eq(8).text());
					const time = clean(tds.eq(9).text());

					return {
						fightId,
						fightUrl: fightLink,
						result,
						fighters,
						stats: {
							knockdowns: [kd1, kd2],
							strikes: [str1, str2],
							takedowns: [td1, td2],
							submissions: [sub1, sub2],
						},
						weightClass,
						method,
						methodDetail,
						round,
						time,
					};
				});

			const result = {
				id,
				name,
				info,
				fights,
				fightCount: fights.length,
				url: `${BASE_URL}/event-details/${id}`,
			};
			// If any fight on the card has a recorded result, the event has
			// happened — cache as historical. Otherwise it's still upcoming.
			const isHistorical = fights.some((f) => f.result !== null);
			const bucket: CacheBucket = isHistorical ? 'eventCompleted' : 'eventUpcoming';
			cacheSet(bucket, id, result);
			c.header('X-Cache', bypass ? 'BYPASS' : 'MISS');
			c.header('Cache-Control', cacheControlHeader(bucket));
			return c.json(result);
		},
	},

	// ─── Route 6: Fight detail (round-by-round) ─────────────────────
	// /api/ufcstats/fight/:id
	{
		method: 'GET',
		path: '/fight/:id',
		description:
			'Fight detail: outcome, both fighters, totals, per-round totals + significant-strike breakdown.',
		browserRequired: false,
		handler: async (c) => {
			const id = (c.req.param() as Record<string, string>).id;
			const err = notFoundIfEmptyId(id);
			if (err) return c.json({ error: err }, 400);

			return cachedJson(c, 'fight', id, async () => {
				const { ok, html, status } = await fetchHtml(`${BASE_URL}/fight-details/${id}`);
				if (!ok) return { error: { error: `Fight page returned ${status}` }, status: 502 };
				const $ = await loadCheerio(html);

				// Header — both fighters (h3 person names with bout result flags)
				const persons = $('div.b-fight-details__person')
					.toArray()
					.map((p) => {
						const $p = $(p);
						const a = $p.find('h3.b-fight-details__person-name a').first();
						const href = a.attr('href') ?? '';
						return {
							name: clean(a.text()),
							id: href.match(/fighter-details\/([a-f0-9]{16})/)?.[1] ?? null,
							nickname: clean($p.find('p.b-fight-details__person-title').text()) || null,
							outcome:
								clean($p.find('i.b-fight-details__person-status').text()).toLowerCase() || null,
						};
					});

				const bout = clean($('i.b-fight-details__fight-title').text());

				// Method/Round/Time/Format/Referee/Details
				const summary: Record<string, string> = {};
				$('p.b-fight-details__text').each((_, p) => {
					const $p = $(p);
					$p.find('i.b-fight-details__label').each((_i, lbl) => {
						const label = clean($(lbl).text())
							.replace(/:$/, '')
							.toLowerCase()
							.replace(/[^a-z0-9]+/g, '_');
						if (!label) return;
						// Sibling text: take the text up to the next label
						const sib = $(lbl).get(0)?.nextSibling;
						let val = '';
						let cur = sib;
						while (cur) {
							const node = cur as { type?: string; nodeType?: number; data?: string };
							if (node.type === 'tag' && (cur as unknown as Element).tagName?.toLowerCase() === 'i')
								break;
							if (node.type === 'text' && typeof node.data === 'string') val += node.data;
							else if (node.type === 'tag') val += $(cur as never).text();
							cur = (cur as unknown as { nextSibling?: unknown }).nextSibling as never;
						}
						const cleaned = clean(val);
						if (cleaned) summary[label] = cleaned;
					});
				});

				// Fight-details page contains 4 <table> elements in a fixed order:
				//   [0] totals summary       — no class on <table>
				//   [1] totals per round     — class="b-fight-details__table js-fight-table"
				//   [2] sig strikes summary  — no class on <table>
				//   [3] sig strikes per round — class="b-fight-details__table js-fight-table"
				// Each table has rows where every <td> holds two <p> values (fighter A | fighter B).
				const allTables = $('table');

				function parseSummaryTable(table: ReturnType<CheerioAPI>): Record<string, string> | null {
					if (table.length === 0) return null;
					const headers = table
						.find('thead th')
						.toArray()
						.map((th) => clean($(th).text()));
					const dataRow = table
						.find('tbody tr.b-fight-details__table-row')
						.toArray()
						.find((r) => $(r).find('td.b-fight-details__table-col').length > 0);
					if (!dataRow) return null;
					const out: Record<string, string> = {};
					$(dataRow)
						.find('td.b-fight-details__table-col')
						.each((i, td) => {
							const ps = $(td).find('p.b-fight-details__table-text');
							const vals = ps.toArray().map((p) => clean($(p).text()));
							out[headers[i] ?? `col_${i}`] = vals.join(' | ');
						});
					return out;
				}

				function parsePerRoundTable(
					table: ReturnType<CheerioAPI>,
				): Array<{ round: string; data: Record<string, string> }> {
					if (table.length === 0) return [];
					const rounds: Array<{ round: string; data: Record<string, string> }> = [];
					let headers: string[] = [];
					let currentRound = '';
					// Walk thead/tbody children in document order. The first thead is the
					// column header row; subsequent theads contain "Round N" labels.
					table.children().each((_, el) => {
						const tagName = (el as { tagName?: string }).tagName?.toLowerCase();
						const $el = $(el);
						if (tagName === 'thead') {
							const text = clean($el.text());
							if (/^Round\s+\d+/i.test(text)) {
								currentRound = text;
							} else {
								headers = $el
									.find('th')
									.toArray()
									.map((th) => clean($(th).text()));
							}
							return;
						}
						if (tagName !== 'tbody') return;
						const dataRow = $el
							.find('tr.b-fight-details__table-row')
							.toArray()
							.find((r) => $(r).find('td.b-fight-details__table-col').length > 0);
						if (!dataRow) return;
						const data: Record<string, string> = {};
						$(dataRow)
							.find('td.b-fight-details__table-col')
							.each((i, td) => {
								const ps = $(td).find('p.b-fight-details__table-text');
								data[headers[i] ?? `col_${i}`] = ps
									.toArray()
									.map((p) => clean($(p).text()))
									.join(' | ');
							});
						rounds.push({ round: currentRound || 'Total', data });
					});
					return rounds;
				}

				const totals = parseSummaryTable(allTables.eq(0));
				const totalsByRound = parsePerRoundTable(allTables.eq(1));
				const sigStrikes = parseSummaryTable(allTables.eq(2));
				const sigStrikesByRound = parsePerRoundTable(allTables.eq(3));

				return {
					data: {
						id,
						bout,
						fighters: persons,
						summary,
						totals,
						totalsByRound,
						sigStrikes,
						sigStrikesByRound,
						url: `${BASE_URL}/fight-details/${id}`,
					},
					status: 200,
				};
			});
		},
	},
];
