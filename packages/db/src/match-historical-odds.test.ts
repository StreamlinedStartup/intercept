import { describe, expect, it } from 'vitest';
import { matchHistoricalFight, normalizeName } from './match-historical-odds-core.js';

const canonicalFights = [
	{
		fightId: 'fight-a',
		fighters: [
			{ id: 'moreno', name: 'Brandon Moreno' },
			{ id: 'royval', name: 'Brandon Royval' },
		],
	},
	{
		fightId: 'fight-b',
		fighters: [
			{ id: 'barcelos', name: 'Raoni Barcelos' },
			{ id: 'quinonez', name: 'Cristian Quinonez' },
		],
	},
	{
		fightId: 'fight-c',
		fighters: [
			{ id: 'lacerda', name: 'Daniel Lacerda' },
			{ id: 'chairez', name: 'Edgar Chairez' },
		],
	},
];

describe('historical odds matching', () => {
	it('normalizes accents and punctuation', () => {
		expect(normalizeName('Raul Rosas Jr.')).toBe('raul rosas');
		expect(normalizeName('Mateus Mendonça')).toBe('mateus mendonca');
		expect(normalizeName('Christian Quiñónez')).toBe('christian quinonez');
	});

	it('matches a swapped source fighter order', () => {
		const match = matchHistoricalFight(
			{ rawFighterA: 'Brandon Royval', rawFighterB: 'Brandon Moreno', isCancelled: false },
			canonicalFights,
		);
		expect(match.status).toBe('matched');
		if (match.status === 'matched') {
			expect(match.fight.fightId).toBe('fight-a');
			expect(match.sourceFighterAToCanonicalId).toBe('royval');
			expect(match.sourceFighterBToCanonicalId).toBe('moreno');
		}
	});

	it('matches spelling and renamed-fighter aliases', () => {
		const accentMatch = matchHistoricalFight(
			{ rawFighterA: 'Christian Quiñónez', rawFighterB: 'Raoni Barcelos', isCancelled: false },
			canonicalFights,
		);
		const renameMatch = matchHistoricalFight(
			{ rawFighterA: 'Edgar Chairez', rawFighterB: 'Daniel da Silva', isCancelled: false },
			canonicalFights,
		);
		const spellingMatch = matchHistoricalFight(
			{ rawFighterA: 'Muhammadjon Naimov', rawFighterB: 'Erik Silva', isCancelled: false },
			[
				{
					fightId: 'fight-d',
					fighters: [
						{ id: 'naimov', name: 'Muhammad Naimov' },
						{ id: 'silva', name: 'Erik Silva' },
					],
				},
			],
		);
		expect(accentMatch.status).toBe('matched');
		expect(renameMatch.status).toBe('matched');
		expect(spellingMatch.status).toBe('matched');
	});

	it('preserves ambiguous matches for review', () => {
		const match = matchHistoricalFight(
			{ rawFighterA: 'Brandon Moreno', rawFighterB: 'Brandon Royval', isCancelled: false },
			[
				canonicalFights[0],
				{
					fightId: 'duplicate',
					fighters: [
						{ id: 'moreno-2', name: 'Brandon Moreno' },
						{ id: 'royval-2', name: 'Brandon Royval' },
					],
				},
			],
		);
		expect(match.status).toBe('ambiguous');
		if (match.status === 'ambiguous') {
			expect(match.candidates).toHaveLength(2);
		}
	});
});
