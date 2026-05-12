import { describe, expect, it } from 'vitest';
import {
	eventNameTokens,
	matchHistoricalFight,
	normalizeEventName,
	normalizeName,
} from './match-historical-odds-core.js';

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
		expect(normalizeName('Michał Oleksiejczuk')).toBe('michal oleksiejczuk');
	});

	it('normalizes FightOdds event aliases to canonical UFCStats event names', () => {
		expect(normalizeEventName('UFC on ESPN 50: Sandhagen vs. Font')).toBe(
			'ufc fight night sandhagen vs font',
		);
		expect(normalizeEventName('UFC on ABC 4: Rozenstruik vs. Almeida')).toBe(
			'ufc fight night rozenstruik vs almeida',
		);
		expect(normalizeEventName('UFC Fight Night 226: Gane vs. Spivak')).toBe(
			'ufc fight night gane vs spivak',
		);
		expect(eventNameTokens(normalizeEventName('UFC Fight Night 226: Gane vs. Spivak'))).toEqual([
			'gane',
			'spivac',
		]);
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

	it('matches FightOdds/UFCStats participant naming differences', () => {
		const rozenstruikMatch = matchHistoricalFight(
			{ rawFighterA: 'Jair Rozenstruik', rawFighterB: 'Shamil Gaziev', isCancelled: false },
			[
				{
					fightId: 'fight-d',
					fighters: [
						{ id: 'rozenstruik', name: 'Jairzinho Rozenstruik' },
						{ id: 'gaziev', name: 'Shamil Gaziev' },
					],
				},
			],
		);
		const particleMatch = matchHistoricalFight(
			{ rawFighterA: 'Vinicius de Oliveira', rawFighterB: 'Benardo Sopaj', isCancelled: false },
			[
				{
					fightId: 'fight-e',
					fighters: [
						{ id: 'oliveira', name: 'Vinicius Oliveira' },
						{ id: 'sopaj', name: 'Benardo Sopaj' },
					],
				},
			],
		);
		const transposedMatch = matchHistoricalFight(
			{ rawFighterA: 'Petr Yan', rawFighterB: 'Yadong Song', isCancelled: false },
			[
				{
					fightId: 'fight-f',
					fighters: [
						{ id: 'yan', name: 'Petr Yan' },
						{ id: 'yadong', name: 'Song Yadong' },
					],
				},
			],
		);
		const shortNameMatch = matchHistoricalFight(
			{ rawFighterA: 'Luiz Philipe Lins', rawFighterB: 'Ion Cutelaba', isCancelled: false },
			[
				{
					fightId: 'fight-g',
					fighters: [
						{ id: 'lins', name: 'Philipe Lins' },
						{ id: 'cutelaba', name: 'Ion Cutelaba' },
					],
				},
			],
		);
		const aliasMatch = matchHistoricalFight(
			{ rawFighterA: 'Carlos Vergara', rawFighterB: 'Asu Almabaev', isCancelled: false },
			[
				{
					fightId: 'fight-h',
					fighters: [
						{ id: 'vergara', name: 'CJ Vergara' },
						{ id: 'almabayev', name: 'Asu Almabayev' },
					],
				},
			],
		);
		expect(rozenstruikMatch.status).toBe('matched');
		expect(particleMatch.status).toBe('matched');
		expect(transposedMatch.status).toBe('matched');
		expect(shortNameMatch.status).toBe('matched');
		expect(aliasMatch.status).toBe('matched');
	});

	it('keeps cancelled source fights reviewable instead of linking them', () => {
		const match = matchHistoricalFight(
			{ rawFighterA: 'Brandon Moreno', rawFighterB: 'Brandon Royval', isCancelled: true },
			canonicalFights,
		);
		expect(match.status).toBe('unmatched');
		expect(match.reason).toBe('source fight is cancelled; canonical linking skipped');
		if (match.status === 'unmatched') {
			expect(match.candidates).toHaveLength(1);
		}
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
