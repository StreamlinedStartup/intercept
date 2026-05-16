export type Over25Indicator = {
	label: string;
	model_version: string;
	model_probability: number | null;
	market_probability: number | null;
	edge_pct: number | null;
	threshold: number;
	candidate: boolean;
	market_pair_count: number;
	training_sample_count: number;
	value_status:
		| 'report_only'
		| 'insufficient_coverage'
		| 'insufficient_training'
		| 'missing_snapshot'
		| 'stale_snapshot';
	value_status_reason: string;
	computed_at: string | null;
	snapshot_status: 'current' | 'stale' | 'missing';
};

export function over25Name(indicator: Over25Indicator | undefined): string {
	if (!indicator) return 'Signal unavailable';
	if (indicator.value_status === 'missing_snapshot') return 'Snapshot missing';
	if (indicator.value_status === 'stale_snapshot') return 'Snapshot stale';
	if (indicator.value_status === 'insufficient_training') return 'Needs training data';
	if (indicator.value_status === 'insufficient_coverage') return 'Market unavailable';
	return indicator.candidate ? 'Candidate active' : 'No signal';
}

export function over25Primary(indicator: Over25Indicator | undefined): string {
	if (!indicator) return 'Run indicator refresh';
	if (indicator.value_status === 'missing_snapshot') return 'Run daily maintenance';
	if (!indicator.model_probability) return 'Need model output';
	const model = `Model ${formatPct(indicator.model_probability)}`;
	const market =
		indicator.market_probability === null
			? 'market unavailable'
			: `market ${formatPct(indicator.market_probability)}`;
	const edge = indicator.edge_pct === null ? '' : `, edge ${formatSignedPct(indicator.edge_pct)}`;
	return `${model}, ${market}${edge}`;
}

export function over25BadgeText(indicator: Over25Indicator): string {
	if (indicator.value_status === 'missing_snapshot') return 'Refresh';
	if (indicator.value_status === 'stale_snapshot') return 'Stale';
	if (indicator.value_status === 'insufficient_training') return 'Need data';
	if (indicator.value_status === 'insufficient_coverage') return 'Need props';
	return indicator.candidate ? 'Report only' : `Below ${formatPct(indicator.threshold)}`;
}

export function over25BadgeTone(indicator: Over25Indicator): 'green' | 'amber' | 'red' | 'neutral' {
	if (indicator.value_status === 'missing_snapshot') return 'neutral';
	if (indicator.value_status === 'stale_snapshot') return 'amber';
	if (indicator.value_status === 'insufficient_training') return 'neutral';
	if (indicator.value_status === 'insufficient_coverage') return 'amber';
	return indicator.candidate ? 'amber' : 'neutral';
}

function formatPct(value: number): string {
	return `${Math.round(value * 100)}%`;
}

function formatSignedPct(value: number): string {
	const pct = Math.round(value * 100);
	return `${pct > 0 ? '+' : ''}${pct}%`;
}
