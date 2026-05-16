import { describe, expect, it } from 'vitest';
import {
	buildMlPredictParams,
	getValueStatus,
	mergeOver25Indicator,
	over25NoVigMarket,
} from './predict';

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

describe('over25NoVigMarket', () => {
	it('averages no-vig Over 2.5 probabilities across complete book pairs', () => {
		expect(
			over25NoVigMarket([
				{
					source_market_id: 'market-1',
					sportsbook_slug: 'book-a',
					outcome_side: 'outcome1',
					implied_probability: 0.6,
				},
				{
					source_market_id: 'market-1',
					sportsbook_slug: 'book-a',
					outcome_side: 'outcome2',
					implied_probability: 0.5,
				},
				{
					source_market_id: 'market-1',
					sportsbook_slug: 'book-b',
					outcome_side: 'outcome1',
					implied_probability: 0.55,
				},
				{
					source_market_id: 'market-1',
					sportsbook_slug: 'book-b',
					outcome_side: 'outcome2',
					implied_probability: 0.55,
				},
			]),
		).toEqual({
			market_probability: (0.6 / 1.1 + 0.5) / 2,
			pair_count: 2,
		});
	});

	it('returns null when no complete two-way market exists', () => {
		expect(
			over25NoVigMarket([
				{
					source_market_id: 'market-1',
					sportsbook_slug: 'book-a',
					outcome_side: 'outcome1',
					implied_probability: 0.6,
				},
			]),
		).toBeNull();
	});
});

describe('mergeOver25Indicator', () => {
	const model = {
		target: 'over_2_5' as const,
		label: 'Over 2.5 rounds',
		model_version: 'locked_over_2_5_positive_log_c1_conf58',
		model_probability: 0.64,
		threshold: 0.58,
		candidate: true,
		value_status: 'report_only' as const,
		value_status_reason:
			'Locked validation passed; live forward tracking required before production betting activation.',
		training_sample_count: 358,
	};

	it('attaches market probability and report-only edge', () => {
		expect(mergeOver25Indicator(model, { market_probability: 0.52, pair_count: 8 })).toEqual({
			target: 'over_2_5',
			label: 'Over 2.5 rounds',
			model_version: 'locked_over_2_5_positive_log_c1_conf58',
			model_probability: 0.64,
			market_probability: 0.52,
			edge_pct: 0.12,
			threshold: 0.58,
			candidate: true,
			market_pair_count: 8,
			training_sample_count: 358,
			value_status: 'report_only',
			value_status_reason:
				'Locked validation passed; live forward tracking required before production betting activation.',
		});
	});

	it('keeps model candidate but marks missing prop market as insufficient coverage', () => {
		expect(mergeOver25Indicator(model, null)).toMatchObject({
			candidate: true,
			market_probability: null,
			edge_pct: null,
			value_status: 'insufficient_coverage',
		});
	});
});
