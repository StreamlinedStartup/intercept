import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, relative, resolve } from 'node:path';

const REPO_ROOT = resolve(import.meta.dirname, '../../..');
const COVERAGE_INPUT = 'data/experiments/historical-odds-target-cohort-baseline.json';
const LEAKAGE_INPUT = 'data/experiments/leakage-audit.json';
const BASELINES_INPUT = 'data/experiments/simple-baselines.json';
const MARKET_GATE_INPUT = 'data/experiments/market-gate-report.json';
const DEFAULT_JSON_OUTPUT = 'data/experiments/historical-odds-corpus-expansion-final-report.json';
const DEFAULT_MARKDOWN_OUTPUT = 'data/experiments/historical-odds-corpus-expansion-final-report.md';

type CoverageReport = {
	generated_at: string;
	report_only: true;
	writes_model_versions: false;
	target_cohort: {
		id: string;
		title: string;
		from: string;
		to: string;
		target_event_count: number;
		import_command: string;
		match_command: string;
		report_command: string;
		rationale: string;
	};
	summary: {
		source_events: number;
		matched_source_events: number;
		target_events: number;
		imported_target_events: number;
		source_fights: number;
		matched_fights: number;
		ambiguous_fights: number;
		unmatched_fights: number;
		cancelled_unmatched_fights: number;
		moneyline_rows: number;
		linked_moneyline_rows: number;
		review_rows: number;
		fight_match_rate: number;
		moneyline_link_rate: number;
	};
	review_reasons: { reason: string; rows: number }[];
};

type LeakageAudit = {
	generated_at: string;
	report_only: true;
	writes_model_versions: false;
	summary: {
		checks: number;
		passed: number;
		failed: number;
	};
};

type BaselineReport = {
	generated_at: string;
	report_only: true;
	writes_model_versions: false;
	market_coverage: {
		samples: number;
		covered_samples: number;
		coverage_rate: number;
	};
	baselines: {
		name: string;
		metrics: {
			count: number;
			accuracy: number;
			log_loss: number;
			brier_score: number;
			roc_auc: number | null;
		};
		simulated_research_roi?: {
			entries: number;
			units: number;
			roi_pct: number;
			status: 'simulated_research_only';
		};
	}[];
};

type MarketGateReport = {
	generated_at: string;
	report_only: true;
	writes_model_versions: false;
	value_status: 'insufficient_coverage' | 'validated' | string;
	value_status_reason: string;
	validation_thresholds: {
		min_fights: number;
		min_market_events: number;
		min_market_roi_delta: number;
	};
	coverage: {
		source_events_imported: number;
		source_events_matched: number;
		source_events_unmatched: number;
		source_fights_imported: number;
		source_fights_matched: number;
		source_fights_unmatched: number;
		moneyline_rows_imported: number;
		moneyline_rows_linked: number;
		scored_events: number;
		scored_fights: number;
	};
	strategies: {
		name: string;
		metrics: {
			count: number;
			accuracy: number;
			log_loss: number;
			brier_score: number;
			roc_auc: number | null;
		};
		simulated_research_roi: {
			entries: number;
			wins: number;
			units: number;
			roi_pct: number;
			status: 'simulated_research_only';
		};
	}[];
};

type FinalReport = {
	generated_at: string;
	report: 'historical-odds-corpus-expansion-final';
	epic: {
		id: 'intercept-vgy0';
		title: 'D2-HOC: Historical odds corpus expansion and entity-resolution gate';
		parent: 'intercept-8mw9';
	};
	report_only: true;
	writes_model_versions: false;
	value_status: string;
	value_status_reason: string;
	model_improvement_unblocked: boolean;
	model_improvement_blockers: string[];
	inputs: {
		coverage_report: string;
		leakage_audit: string;
		baseline_report: string;
		market_gate_report: string;
	};
	coverage: CoverageReport['summary'] & MarketGateReport['coverage'];
	target_cohort: CoverageReport['target_cohort'];
	review_reasons: CoverageReport['review_reasons'];
	verification: {
		leakage_audit: LeakageAudit['summary'];
		market_coverage: BaselineReport['market_coverage'];
		market_favorite: BaselineReport['baselines'][number] | null;
		market_gate_thresholds: MarketGateReport['validation_thresholds'];
		market_gate_strategies: MarketGateReport['strategies'];
	};
	conclusion: string;
};

async function main() {
	const coverage = await readJson<CoverageReport>(COVERAGE_INPUT);
	const leakage = await readJson<LeakageAudit>(LEAKAGE_INPUT);
	const baselines = await readJson<BaselineReport>(BASELINES_INPUT);
	const marketGate = await readJson<MarketGateReport>(MARKET_GATE_INPUT);
	const report = buildFinalReport(coverage, leakage, baselines, marketGate);
	const jsonOutput = resolveRepoPath(DEFAULT_JSON_OUTPUT);
	const markdownOutput = resolveRepoPath(DEFAULT_MARKDOWN_OUTPUT);

	await mkdir(dirname(jsonOutput), { recursive: true });
	await mkdir(dirname(markdownOutput), { recursive: true });
	await writeFile(jsonOutput, `${JSON.stringify(report, null, 2)}\n`);
	await writeFile(markdownOutput, `${renderMarkdown(report)}\n`);

	console.log(
		JSON.stringify(
			{
				output: displayPath(jsonOutput),
				markdown: displayPath(markdownOutput),
				value_status: report.value_status,
				model_improvement_unblocked: report.model_improvement_unblocked,
				scored_fights: report.coverage.scored_fights,
				scored_events: report.coverage.scored_events,
			},
			null,
			2,
		),
	);
}

function buildFinalReport(
	coverage: CoverageReport,
	leakage: LeakageAudit,
	baselines: BaselineReport,
	marketGate: MarketGateReport,
): FinalReport {
	const minScoredEvents = marketGate.validation_thresholds.min_market_events;
	const eventShortfall = Math.max(0, minScoredEvents - marketGate.coverage.scored_events);
	const marketFavorite =
		baselines.baselines.find((baseline) => baseline.name === 'market_favorite') ?? null;
	const blockers = [
		`Market gate remains ${marketGate.value_status}: ${marketGate.value_status_reason}`,
		`Resolve at least ${eventShortfall} additional market-covered scored UFC events to reach ${minScoredEvents} scored events.`,
		`Reduce or explain ${coverage.summary.review_rows} unresolved historical odds review rows before using the corpus for model-value claims.`,
	];

	return {
		generated_at: new Date().toISOString(),
		report: 'historical-odds-corpus-expansion-final',
		epic: {
			id: 'intercept-vgy0',
			title: 'D2-HOC: Historical odds corpus expansion and entity-resolution gate',
			parent: 'intercept-8mw9',
		},
		report_only: true,
		writes_model_versions: false,
		value_status: marketGate.value_status,
		value_status_reason: marketGate.value_status_reason,
		model_improvement_unblocked: marketGate.value_status === 'validated',
		model_improvement_blockers: marketGate.value_status === 'validated' ? [] : blockers,
		inputs: {
			coverage_report: COVERAGE_INPUT,
			leakage_audit: LEAKAGE_INPUT,
			baseline_report: BASELINES_INPUT,
			market_gate_report: MARKET_GATE_INPUT,
		},
		coverage: {
			...coverage.summary,
			...marketGate.coverage,
		},
		target_cohort: coverage.target_cohort,
		review_reasons: coverage.review_reasons,
		verification: {
			leakage_audit: leakage.summary,
			market_coverage: baselines.market_coverage,
			market_favorite: marketFavorite,
			market_gate_thresholds: marketGate.validation_thresholds,
			market_gate_strategies: marketGate.strategies,
		},
		conclusion:
			marketGate.value_status === 'validated'
				? 'The market gate passed; model-improvement work can proceed under the validated gate.'
				: 'Model-improvement work remains blocked for value claims. The corpus now has enough scored fights but only 26 scored market-covered events, below the 30-event validation threshold.',
	};
}

function renderMarkdown(report: FinalReport): string {
	const pct = (value: number | null | undefined) =>
		typeof value === 'number' ? `${(value * 100).toFixed(1)}%` : 'n/a';
	const units = (value: number | undefined) =>
		typeof value === 'number' ? value.toFixed(2) : 'n/a';
	const strategyRows = report.verification.market_gate_strategies
		.map(
			(strategy) =>
				`| ${strategy.name} | ${strategy.metrics.count} | ${pct(strategy.metrics.accuracy)} | ${pct(
					strategy.simulated_research_roi.roi_pct,
				)} | ${units(strategy.simulated_research_roi.units)} | ${strategy.simulated_research_roi.status} |`,
		)
		.join('\n');
	const reasonRows = report.review_reasons
		.map((reason) => `| ${reason.reason} | ${reason.rows} |`)
		.join('\n');
	const blockers =
		report.model_improvement_blockers.length > 0
			? report.model_improvement_blockers.map((blocker) => `- ${blocker}`).join('\n')
			: '- None; market gate passed.';

	return `# D2-HOC Corpus Expansion Final Report

Generated: ${report.generated_at}

Report-only: ${String(report.report_only)}
Writes model_versions: ${String(report.writes_model_versions)}
Value status: ${report.value_status}
Model improvement unblocked: ${String(report.model_improvement_unblocked)}

## Conclusion

${report.conclusion}

${report.value_status_reason}

## Coverage

| Metric | Value |
| --- | ---: |
| Target events | ${report.coverage.target_events} |
| Imported target events | ${report.coverage.imported_target_events} |
| Matched source events | ${report.coverage.matched_source_events}/${report.coverage.source_events} |
| Scored market-covered events | ${report.coverage.scored_events}/${report.verification.market_gate_thresholds.min_market_events} |
| Scored market-covered fights | ${report.coverage.scored_fights}/${report.verification.market_gate_thresholds.min_fights} |
| Source fights imported | ${report.coverage.source_fights_imported} |
| Source fights matched | ${report.coverage.source_fights_matched} |
| Fight match rate | ${pct(report.coverage.fight_match_rate)} |
| Moneyline rows imported | ${report.coverage.moneyline_rows_imported} |
| Moneyline rows linked | ${report.coverage.moneyline_rows_linked} |
| Moneyline link rate | ${pct(report.coverage.moneyline_link_rate)} |
| Review rows | ${report.coverage.review_rows} |

## Review Reasons

| Reason | Rows |
| --- | ---: |
${reasonRows}

## Verification

| Check | Result |
| --- | --- |
| Leakage audit | ${report.verification.leakage_audit.passed}/${report.verification.leakage_audit.checks} passed |
| Baseline samples | ${report.verification.market_coverage.samples} |
| Market-covered baseline samples | ${report.verification.market_coverage.covered_samples} |
| Market coverage rate | ${pct(report.verification.market_coverage.coverage_rate)} |
| Market favorite accuracy | ${pct(report.verification.market_favorite?.metrics.accuracy)} |
| Market favorite simulated ROI | ${pct(report.verification.market_favorite?.simulated_research_roi?.roi_pct)} |

## Market Gate Strategies

| Strategy | Fights | Accuracy | Simulated ROI | Units | Status |
| --- | ---: | ---: | ---: | ---: | --- |
${strategyRows}

## Remaining Blockers

${blockers}

## Inputs

- ${report.inputs.coverage_report}
- ${report.inputs.leakage_audit}
- ${report.inputs.baseline_report}
- ${report.inputs.market_gate_report}
`;
}

async function readJson<T>(path: string): Promise<T> {
	const raw = await readFile(resolveRepoPath(path), 'utf8');
	return JSON.parse(raw) as T;
}

function resolveRepoPath(path: string) {
	return resolve(REPO_ROOT, path);
}

function displayPath(path: string) {
	return relative(REPO_ROOT, path);
}

main().catch((error) => {
	console.error(error);
	process.exitCode = 1;
});
