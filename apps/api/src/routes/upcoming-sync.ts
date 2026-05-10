import { db, events, fighters, fightResults, fights } from '@interceptor/db';
import type { Hono } from 'hono';

type UfcstatsUpcomingResponse = {
	events: Array<{ id: string; name: string; date: string; location: string | null }>;
};

type UfcstatsEventDetail = {
	id: string;
	name: string;
	info: { date?: string; location?: string } & Record<string, string>;
	fights: Array<{
		fightId: string | null;
		fighters: Array<{ id: string | null; name: string }>;
		weightClass: string;
	}>;
};

type SyncResult = {
	events_seen: number;
	events_upserted: number;
	fights_seen: number;
	fights_upserted: number;
	fighters_upserted: number;
	pending_participants_upserted: number;
	skipped_fights: Array<{ event_id: string; reason: string; fighters: string[] }>;
};

export function registerUpcomingSyncRoutes(app: Hono): void {
	app.post('/api/predict/sync/upcoming-cards', async (c) => {
		const origin = new URL(c.req.url).origin;
		const result = await syncUpcomingCards(origin);
		return c.json(result);
	});
}

async function syncUpcomingCards(origin: string): Promise<SyncResult> {
	const upcoming = await fetchInternalJson<UfcstatsUpcomingResponse>(
		origin,
		'/api/ufcstats/events/upcoming?refresh=1',
	);
	const result: SyncResult = {
		events_seen: upcoming.events.length,
		events_upserted: 0,
		fights_seen: 0,
		fights_upserted: 0,
		fighters_upserted: 0,
		pending_participants_upserted: 0,
		skipped_fights: [],
	};

	for (const upcomingEvent of upcoming.events) {
		const detail = await fetchInternalJson<UfcstatsEventDetail>(
			origin,
			`/api/ufcstats/event/${upcomingEvent.id}?refresh=1`,
		);
		const eventDate = parseUfcstatsDate(detail.info.date ?? upcomingEvent.date);
		if (!eventDate) {
			result.skipped_fights.push({
				event_id: upcomingEvent.id,
				reason: 'event date could not be parsed',
				fighters: [],
			});
			continue;
		}

		await db
			.insert(events)
			.values({
				id: detail.id,
				name: detail.name || upcomingEvent.name,
				date: eventDate,
				location: detail.info.location ?? upcomingEvent.location ?? null,
				completed: false,
				promotion: 'ufc',
			})
			.onConflictDoUpdate({
				target: events.id,
				set: {
					name: detail.name || upcomingEvent.name,
					date: eventDate,
					location: detail.info.location ?? upcomingEvent.location ?? null,
					completed: false,
					promotion: 'ufc',
				},
			});
		result.events_upserted++;

		for (let fightIndex = 0; fightIndex < detail.fights.length; fightIndex++) {
			const cardFight = detail.fights[fightIndex];
			result.fights_seen++;
			const usableFighters = cardFight.fighters
				.map((fighter) => ({
					id: fighter.id ?? derivedFighterId(fighter.name),
					name: fighter.name,
				}))
				.filter((fighter) => fighter.id && fighter.name);
			if (usableFighters.length !== 2) {
				result.skipped_fights.push({
					event_id: detail.id,
					reason: 'fight does not have exactly two parseable fighters',
					fighters: cardFight.fighters.map((fighter) => fighter.name).filter(Boolean),
				});
				continue;
			}

			const [fighterA, fighterB] = usableFighters as [
				{ id: string; name: string },
				{ id: string; name: string },
			];
			for (const fighter of [fighterA, fighterB]) {
				await db
					.insert(fighters)
					.values({ id: fighter.id, name: fighter.name })
					.onConflictDoUpdate({
						target: fighters.id,
						set: { name: fighter.name },
					});
				result.fighters_upserted++;
			}

			const fightId =
				cardFight.fightId ?? derivedFightId(detail.id, fightIndex, fighterA.id, fighterB.id);
			await db
				.insert(fights)
				.values({
					id: fightId,
					eventId: detail.id,
					weightClass: normalizeWeightClass(cardFight.weightClass),
					scheduledRounds: fightIndex === 0 ? 5 : 3,
					isHeadliner: fightIndex === 0,
				})
				.onConflictDoUpdate({
					target: fights.id,
					set: {
						eventId: detail.id,
						weightClass: normalizeWeightClass(cardFight.weightClass),
						scheduledRounds: fightIndex === 0 ? 5 : 3,
						isHeadliner: fightIndex === 0,
					},
				});
			result.fights_upserted++;

			await db
				.insert(fightResults)
				.values([
					{
						fightId,
						fighterId: fighterA.id,
						opponentId: fighterB.id,
						outcome: 'nc',
					},
					{
						fightId,
						fighterId: fighterB.id,
						opponentId: fighterA.id,
						outcome: 'nc',
					},
				])
				.onConflictDoNothing();
			result.pending_participants_upserted += 2;
		}
	}

	return result;
}

async function fetchInternalJson<T>(origin: string, path: string): Promise<T> {
	const res = await fetch(`${origin}${path}`);
	const text = await res.text();
	if (!res.ok) {
		throw new Error(`${path} returned ${res.status}: ${text.slice(0, 300)}`);
	}
	return JSON.parse(text) as T;
}

function parseUfcstatsDate(value: string | undefined): string | null {
	if (!value || value === '--') return null;
	const date = new Date(value);
	if (Number.isNaN(date.getTime())) return null;
	return date.toISOString().slice(0, 10);
}

function normalizeWeightClass(value: string): string | null {
	const cleaned = value.trim().toLowerCase().replace(/\s+/g, ' ');
	return cleaned || null;
}

function slug(value: string): string {
	return value
		.toLowerCase()
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-+|-+$/g, '');
}

function derivedFighterId(name: string): string {
	const fighterSlug = slug(name);
	if (!fighterSlug) throw new Error('Cannot derive fighter id from an empty name');
	return `ufcstats:pending-fighter:${fighterSlug}`;
}

function derivedFightId(
	eventId: string,
	fightIndex: number,
	fighterAId: string,
	fighterBId: string,
): string {
	const pair = [fighterAId, fighterBId].sort().join('-vs-');
	return `ufcstats:pending-fight:${eventId}:${fightIndex}:${pair}`;
}
