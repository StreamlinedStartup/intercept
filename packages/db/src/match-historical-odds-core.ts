export type CanonicalFight = {
	fightId: string;
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
	['cristian quinonez', ['christian quinonez']],
	['daniel lacerda', ['daniel da silva']],
	['muhammad naimov', ['muhammadjon naimov']],
	['ronaldo rodriguez', ['luis rodriguez']],
	['yazmin jauregui', ['yasmine jauregui']],
]);

export function matchHistoricalFight(
	historicalFight: { rawFighterA: string; rawFighterB: string; isCancelled: boolean },
	canonicalFights: CanonicalFight[],
): FightMatch {
	const sourceA = nameKeys(historicalFight.rawFighterA);
	const sourceB = nameKeys(historicalFight.rawFighterB);
	const candidates = canonicalFights
		.map((fight) => ({ fight, mapping: mapFighters(sourceA, sourceB, fight) }))
		.filter((candidate) => candidate.mapping !== null);

	if (candidates.length === 1) {
		const [candidate] = candidates;
		return {
			status: 'matched',
			reason: candidate.mapping?.swapped
				? 'matched by normalized sorted fighter pair with swapped source order'
				: 'matched by normalized sorted fighter pair',
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

export function normalizeName(value: string): string {
	return value
		.normalize('NFKD')
		.replace(/[\u0300-\u036f]/g, '')
		.toLowerCase()
		.replace(/\b(jr|sr|ii|iii|iv)\b\.?/g, '')
		.replace(/[^a-z0-9]+/g, ' ')
		.trim()
		.replace(/\s+/g, ' ');
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
	const keys = new Set([normalized]);
	for (const [canonical, aliases] of NAME_ALIASES) {
		if (canonical === normalized || aliases.includes(normalized)) {
			keys.add(canonical);
			for (const alias of aliases) {
				keys.add(alias);
			}
		}
	}
	return [...keys];
}

function intersects(left: string[], right: string[]): boolean {
	const rightSet = new Set(right);
	return left.some((value) => rightSet.has(value));
}
