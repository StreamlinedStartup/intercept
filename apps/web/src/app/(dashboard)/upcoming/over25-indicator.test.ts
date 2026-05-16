import { describe, expect, it } from 'vitest';
import {
	type Over25Indicator,
	over25BadgeText,
	over25BadgeTone,
	over25Name,
	over25Primary,
} from './over25-indicator';

const base: Over25Indicator = {
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
	value_status_reason: 'Snapshot-backed report-only indicator.',
	computed_at: '2026-05-16T10:00:00.000Z',
	snapshot_status: 'current',
};

describe('Over 2.5 indicator UI copy', () => {
	it('preserves the active candidate presentation', () => {
		expect(over25Name(base)).toBe('Candidate active');
		expect(over25Primary(base)).toBe('Model 64%, market 52%, edge +12%');
		expect(over25BadgeText(base)).toBe('Report only');
		expect(over25BadgeTone(base)).toBe('amber');
	});

	it('shows a clear missing snapshot state', () => {
		const indicator = { ...base, value_status: 'missing_snapshot' as const };
		expect(over25Name(indicator)).toBe('Snapshot missing');
		expect(over25Primary(indicator)).toBe('Run daily maintenance');
		expect(over25BadgeText(indicator)).toBe('Refresh');
		expect(over25BadgeTone(indicator)).toBe('neutral');
	});

	it('shows a clear stale snapshot state', () => {
		const indicator = { ...base, value_status: 'stale_snapshot' as const };
		expect(over25Name(indicator)).toBe('Snapshot stale');
		expect(over25BadgeText(indicator)).toBe('Stale');
		expect(over25BadgeTone(indicator)).toBe('amber');
	});
});
