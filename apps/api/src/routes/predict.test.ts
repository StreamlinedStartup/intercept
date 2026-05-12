import { describe, expect, it } from 'vitest';
import { buildMlPredictParams, getValueStatus } from './predict';

describe('buildMlPredictParams', () => {
	it('forwards target fight weight class to ml.predict', () => {
		expect(
			buildMlPredictParams(
				{
					event_date: new Date('2026-06-01T12:00:00.000Z'),
					weight_class: 'Welterweight',
					fighter_id: 'fighter-a',
				},
				{ fighter_id: 'fighter-b' },
			),
		).toEqual({
			fighter_a_id: 'fighter-a',
			fighter_b_id: 'fighter-b',
			fight_date: '2026-06-01',
			weight_class: 'Welterweight',
		});
	});
});

describe('getValueStatus', () => {
	it('marks matched market comparisons as research-only until validation gates pass', () => {
		expect(getValueStatus(true)).toEqual({
			status: 'research_only',
			reason:
				'Edge and ROI are simulated research metrics until leakage audits, baselines, and market-gated validation pass.',
		});
	});

	it('marks missing two-sided odds as insufficient coverage', () => {
		expect(getValueStatus(false)).toEqual({
			status: 'insufficient_coverage',
			reason: 'Matched two-sided market odds are required before edge can be evaluated.',
		});
	});
});
