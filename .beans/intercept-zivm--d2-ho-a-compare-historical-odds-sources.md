---
# intercept-zivm
title: 'D2-HO-A: Discover FightOdds and compare historical odds sources'
status: completed
type: task
priority: normal
created_at: 2026-05-11T13:31:22Z
updated_at: 2026-05-11T17:46:00Z
parent: intercept-5rw9
blocked_by:
    - intercept-qizd
---

Acceptance criteria:
- [x] Inspect FightOdds.io with Intercept/browser traffic discovery and agent-browser.
- [x] Check robots.txt, terms, and rate-limit posture before scraping.
- [x] Determine whether the event and odds pages are server-rendered, embedded JSON, API-backed, or JS-rendered.
- [x] Identify event index/list routes, event detail routes, odds routes, pagination, stable source IDs, and query parameters.
- [x] Capture the technical shape for UFC Fight Night 237 / Moreno vs Royval 2 event and odds pages.
- [x] Compare ESPN, Covers, and FightMatrix fallback viability for the same event.
- [x] Recommend whether FightOdds.io should remain the primary source before schema/import work starts.

Candidate URLs:
- https://fightodds.io/mma-events/5362/ufc-fight-night-237-moreno-vs-royval-2
- https://fightodds.io/mma-events/5362/ufc-fight-night-237-moreno-vs-royval-2/odds
- https://www.espn.com/mma/fightcenter/_/id/600041054
- https://www.covers.com/sport/mma/ufc/card-ufc-fight-night-odds-6472
- https://www.fightmatrix.com/2024/02/19/select-fight-matrix-program-ufc-fight-night-moreno-vs-royval-2-02-23-2024/

Verification:
- Save discovery notes in the bean summary.
- Include enough request/selector evidence to justify the source recommendation.
- Do not implement an importer in this task.

## Summary of Changes

Discovery ran against FightOdds with the repo browser traffic path and
agent-browser:

- API server started with `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor BROWSER_AUTO_START=false pnpm --filter @interceptor/api dev`.
- Browser traffic capture connected through `./scripts/connect-browser.sh --profile fightodds --url https://fightodds.io --port 3001`.
- agent-browser confirmed the rendered homepage, target event odds page, terms page, and fallback source pages.

Source posture:

- `https://fightodds.io/robots.txt` returns `404`, so no robots policy was found.
- `https://fightodds.io/terms-of-service` is SPA-rendered. It says the service is for personal, noncommercial use; it does not expose an explicit robots-style API policy in the rendered text. Treat imports as research-only unless the project gets permission or keeps usage very low and source-attributed.
- Cloudflare is present (`server: cloudflare`, `/cdn-cgi/challenge-platform`, `/cdn-cgi/rum`), but normal browser and direct GraphQL replay worked. Keep request volume conservative.

Transport discovery:

| Transport | Present? | Evidence |
| --- | --- | --- |
| Embedded JSON | No | HTML is a shell with `<div id="app"></div>` and `/app.bundle.js`; no `__NEXT_DATA__` or equivalent was needed for odds data. |
| JSON API (XHR) | Yes | Browser traffic captured repeated `POST https://api.fightodds.io/gql` with `Content-Type: application/json` and `200` responses. |
| GraphQL | Yes | Captured named operations include `EventsRecentQuery`, `EventsHeaderEventQuery`, `EventOddsQuery`, `EventFightsQuery`, `FightOddsQuery`, and many Relay-style fragments. |
| WebSocket | No evidence for odds/event pages | Bundle contains generic `WebSocket` strings, but page traffic for homepage, recent events, and event odds used HTTP GraphQL. |
| HLS/Media | No evidence | No `.m3u8` or media transport was relevant to event/odds pages. |
| gRPC-Web | No evidence | No gRPC-web requests or content types appeared. |
| SSE | No evidence | No `EventSource` request was observed in event/odds traffic. |
| Encoded/Binary | No evidence for odds data | Odds/event payloads are ordinary JSON GraphQL responses. |

Access gap:

| Endpoint | Browser status | Direct HTTP status | Gap? |
| --- | --- | --- | --- |
| `POST https://api.fightodds.io/gql` with captured `EventOddsQuery` body | 200 | 200 | No |
| `POST https://api.fightodds.io/gql` with captured `EventsRecentQuery` page-2 body | 200 | 200 | No |

Relevant GraphQL routes and fields:

- Event list: `EventsRecentQuery($after, $first, $dateGte, $dateLt, $orderBy)` calls `allEvents(first, after, date_Gte, date_Lt, orderBy)` and returns `edges[].node.{id,name,pk,slug,date,venue,city,promotion,poster,posterWide}`, plus Relay `cursor` and `pageInfo.{hasNextPage,endCursor}`.
- Event detail header: `EventsHeaderEventQuery($eventPk)` returns `event{name,slug,date,venue,city,poster,promotion{id,slug,shortName}}`.
- Event odds: `EventOddsQuery($eventPk)` returns `eventOfferTable(pk)` with stable event `pk`, event `slug`, `fightOffers.edges[].node.{id,slug,isCancelled,propCount,bestOdds1,bestOdds2}`, both fighters `{id,firstName,lastName,slug}`, and `straightOffers.edges[].node.{id,sportsbook{id,shortName,slug},outcome1{id,odds,oddsPrev},outcome2{id,odds,oddsPrev}}`.
- Event-list pagination is Relay cursor pagination. Page 1 for recent events used `after: null, first: 10, dateLt: "2026-05-11", orderBy: "-date"` and returned `endCursor: "YXJyYXljb25uZWN0aW9uOjk="`. Direct replay with that cursor returned the next 10 events and a new `endCursor`.

Anchor event evidence:

- Target URL: `https://fightodds.io/mma-events/5362/ufc-fight-night-237-moreno-vs-royval-2/odds`.
- Stable source event ID: `pk: 5362`; GraphQL global ID `RXZlbnROb2RlOjUzNjI=` for event header and `RXZlbnRPZmZlclRhYmxlTm9kZTo1MzYy` for the offer table.
- Event metadata: `UFC Fight Night 237: Moreno vs. Royval 2`, date `2024-02-24`, venue `Arena CDMX`, city `Mexico City, Mexico`, promotion `UFC`.
- Rendered odds table included Brandon Moreno vs Brandon Royval and multiple sportsbooks. Captured GraphQL included sportsbook-level moneylines and `oddsPrev`; it did not expose clear open/close timestamp semantics in this query.
- Cancelled bouts appear in the same `fightOffers` list with `isCancelled: true`, so the importer must preserve and filter by status explicitly.

Fallback comparison:

- ESPN fightcenter page is viable for results/card context, but no sportsbook-level historical odds were visible for the anchor event.
- Covers candidate URL redirected to current UFC content instead of preserving the requested historical card; it is a poor primary source for this slice.
- FightMatrix page is viable as a secondary sanity check because it shows per-fight aggregate `Betting Odds` lines for the anchor event, but it lacks sportsbook-level rows, source IDs, and timestamp/line-history metadata.

Recommendation:

FightOdds.io should remain the primary source for the next schema/import task. It has stable event IDs, direct GraphQL event-list and event-odds queries, sportsbook-level moneyline rows, source fight/fighter IDs, and repeatable direct HTTP access. The schema design should record source query name, source event `pk`, source global IDs, event/fight/fighter slugs, sportsbook IDs/slugs, `odds`, `oddsPrev`, raw GraphQL metadata, and an explicit timestamp-semantics note because the discovered odds query proves current/previous line fields but not true open/close history.
