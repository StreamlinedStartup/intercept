export type CanonicalFight = {
	fightId: string;
	weightClass?: string | null;
	fighters: Array<{ id: string; name: string }>;
};

export type FightMatch =
	| {
			status: 'matched';
			reason: string;
			fight: CanonicalFight;
			sourceFighterAToCanonicalId: string;
			sourceFighterBToCanonicalId: string;
	  }
	| {
			status: 'unmatched' | 'ambiguous';
			reason: string;
			candidates: CanonicalFight[];
	  };

const NAME_ALIASES = new Map<string, string[]>([
	['asu almabayev', ['asu almabaev']],
	['carlos vergara', ['cj vergara']],
	['cristian quinonez', ['christian quinonez']],
	['daniel lacerda', ['daniel da silva']],
	['dontale mayes', ['don tale mayes']],
	['jailton almeida', ['jailton junior']],
	['jairzinho rozenstruik', ['jair rozenstruik']],
	['muhammad naimov', ['muhammadjon naimov']],
	['ronaldo rodriguez', ['luis rodriguez']],
	['yazmin jauregui', ['yasmine jauregui']],
]);

const PARTICLES = new Set(['da', 'de', 'del', 'do', 'dos', 'das']);
const EVENT_TOKEN_ALIASES = new Map([['spivak', 'spivac']]);

export function matchHistoricalFight(
	historicalFight: { rawFighterA: string; rawFighterB: string; isCancelled: boolean },
	canonicalFights: CanonicalFight[],
): FightMatch {
	const sourceA = nameKeys(historicalFight.rawFighterA);
	const sourceB = nameKeys(historicalFight.rawFighterB);
	const candidates = canonicalFights
		.map((fight) => ({ fight, mapping: mapFighters(sourceA, sourceB, fight) }))
		.filter((candidate) => candidate.mapping !== null);

	if (historicalFight.isCancelled) {
		return {
			status: 'unmatched',
			reason: candidates.length
				? 'source fight is cancelled; canonical linking skipped'
				: 'source fight is cancelled and no canonical fight pair exists on the completed event',
			candidates: candidates.map((candidate) => candidate.fight),
		};
	}

	if (candidates.length === 1) {
		const [candidate] = candidates;
		return {
			status: 'matched',
			reason: candidate.mapping?.swapped
				? 'matched by normalized participant keys with swapped source order'
				: 'matched by normalized participant keys',
			fight: candidate.fight,
			sourceFighterAToCanonicalId: candidate.mapping?.fighterAId ?? '',
			sourceFighterBToCanonicalId: candidate.mapping?.fighterBId ?? '',
		};
	}

	if (candidates.length > 1) {
		return {
			status: 'ambiguous',
			reason: 'multiple canonical fights matched normalized fighter pair',
			candidates: candidates.map((candidate) => candidate.fight),
		};
	}

	const partialCandidates = canonicalFights.filter((fight) =>
		fight.fighters.some((fighter) => intersects(nameKeys(fighter.name), sourceA.concat(sourceB))),
	);
	return {
		status: 'unmatched',
		reason: historicalFight.isCancelled
			? 'source fight is cancelled and no canonical fight pair exists on the completed event'
			: 'no canonical fight matched normalized fighter pair',
		candidates: partialCandidates,
	};
}

export function countHistoricalFightParticipantMatches(
	historicalFights: Array<{ rawFighterA: string; rawFighterB: string; isCancelled: boolean }>,
	canonicalFights: CanonicalFight[],
): number {
	return historicalFights
		.map((fight) => matchHistoricalFight(fight, canonicalFights))
		.filter((match) => match.status === 'matched').length;
}

export function normalizeName(value: string): string {
	return value
		.replace(/[łŁ]/g, 'l')
		.normalize('NFKD')
		.replace(/[\u0300-\u036f]/g, '')
		.toLowerCase()
		.replace(/\b(jr|sr|ii|iii|iv)\b\.?/g, '')
		.replace(/[^a-z0-9]+/g, ' ')
		.trim()
		.replace(/\s+/g, ' ');
}

export function normalizeEventName(value: string): string {
	return normalizeName(value)
		.replace(/\bufc on (espn|abc) \d+\b/g, 'ufc fight night')
		.replace(/\bufc fight night \d+\b/g, 'ufc fight night');
}

export function eventNameTokens(normalizedEventName: string): string[] {
	return normalizedEventName
		.split(' ')
		.filter(
			(token) => !['ufc', 'fight', 'night', 'vs'].includes(token) && Number.isNaN(Number(token)),
		)
		.map((token) => EVENT_TOKEN_ALIASES.get(token) ?? token);
}

function mapFighters(sourceA: string[], sourceB: string[], fight: CanonicalFight) {
	const [canonicalA, canonicalB] = fight.fighters;
	const canonicalAKeys = nameKeys(canonicalA.name);
	const canonicalBKeys = nameKeys(canonicalB.name);
	if (intersects(sourceA, canonicalAKeys) && intersects(sourceB, canonicalBKeys)) {
		return { fighterAId: canonicalA.id, fighterBId: canonicalB.id, swapped: false };
	}
	if (intersects(sourceA, canonicalBKeys) && intersects(sourceB, canonicalAKeys)) {
		return { fighterAId: canonicalB.id, fighterBId: canonicalA.id, swapped: true };
	}
	return null;
}

function nameKeys(value: string): string[] {
	const normalized = normalizeName(value);
	const keys = new Set([normalized, sortedNameKey(normalized), withoutParticles(normalized)]);
	const tokens = normalized.split(' ').filter(Boolean);
	if (tokens.length > 2) {
		keys.add(tokens.slice(1).join(' '));
		keys.add(sortedNameKey(tokens.slice(1).join(' ')));
	}
	for (const [canonical, aliases] of NAME_ALIASES) {
		if (canonical === normalized || aliases.includes(normalized)) {
			keys.add(canonical);
			keys.add(sortedNameKey(canonical));
			keys.add(withoutParticles(canonical));
			for (const alias of aliases) {
				keys.add(alias);
				keys.add(sortedNameKey(alias));
				keys.add(withoutParticles(alias));
			}
		}
	}
	return [...keys].filter(Boolean);
}

function intersects(left: string[], right: string[]): boolean {
	const rightSet = new Set(right);
	return left.some((value) => rightSet.has(value));
}

function sortedNameKey(value: string): string {
	return value.split(' ').filter(Boolean).sort().join(' ');
}

function withoutParticles(value: string): string {
	return value
		.split(' ')
		.filter((token) => !PARTICLES.has(token))
		.join(' ');
}
