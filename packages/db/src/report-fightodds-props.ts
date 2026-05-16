import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { sql } from './client.js';

const REPO_ROOT = resolve(import.meta.dirname, '../../..');
const DEFAULT_JSON_OUTPUT = 'data/experiments/fightodds-prop-coverage.json';
const DEFAULT_MARKDOWN_OUTPUT = 'data/experiments/fightodds-prop-coverage.md';

type PropEventCoverage = {
	source_event_id: string;
	raw_name: string;
	event_date: string;
	canonical_event_id: string | null;
	source_fights: number;
	matched_fights: number;
	distance_markets: number;
	prop_rows: number;
	linked_prop_rows: number;
	source_current_rows: number;
	source_previous_rows: number;
};

type OutcomeCoverage = {
	outcome_side: string;
	is_not: boolean;
	raw_outcome_name: string;
	rows: number;
};

type PropCoverageReport = {
	generated_at: string;
	report: 'fightodds-prop-coverage';
	report_only: true;
	writes_model_versions: false;
	summary: {
		source_events: number;
		source_fights: number;
		matched_fights: number;
		distance_markets: number;
		prop_rows: number;
		linked_prop_rows: number;
		source_current_rows: number;
		source_previous_rows: number;
		fight_match_rate: number | null;
		prop_link_rate: number | null;
		decision_finish_baselines_ready: boolean;
	};
	timestamp_limitations: string[];
	readiness_notes: string[];
	events: PropEventCoverage[];
	outcomes: OutcomeCoverage[];
};

async function main() {
	const args = process.argv.slice(2);
	const output = resolveRepoPath(readArg(args, '--output') ?? DEFAULT_JSON_OUTPUT);
	const markdown = resolveRepoPath(readArg(args, '--markdown') ?? DEFAULT_MARKDOWN_OUTPUT);
	try {
		const report = await buildPropCoverageReport();
		await mkdir(dirname(output), { recursive: true });
		await mkdir(dirname(markdown), { recursive: true });
		await writeFile(output, `${JSON.stringify(report, null, 2)}\n`);
		await writeFile(markdown, `${renderMarkdown(report)}\n`);
		console.log(
			JSON.stringify(
				{
					output: displayPath(output),
					markdown: displayPath(markdown),
					summary: report.summary,
				},
				null,
				2,
			),
		);
	} finally {
		await sql.end();
	}
}

export async function buildPropCoverageReport(): Promise<PropCoverageReport> {
	const events = (await sql`
		SELECT
			hoe.source_event_id,
			hoe.raw_name,
			hoe.event_date::text AS event_date,
			hoe.canonical_event_id,
			count(DISTINCT hof.id)::int AS source_fights,
			count(DISTINCT hof.id) FILTER (WHERE hof.canonical_fight_id IS NOT NULL)::int AS matched_fights,
			count(DISTINCT hpo.source_market_id)::int AS distance_markets,
			count(hpo.id)::int AS prop_rows,
			count(hpo.id) FILTER (WHERE hof.canonical_fight_id IS NOT NULL)::int AS linked_prop_rows,
			count(hpo.id) FILTER (WHERE hpo.line_kind = 'source_current')::int AS source_current_rows,
			count(hpo.id) FILTER (WHERE hpo.line_kind = 'source_previous')::int AS source_previous_rows
		FROM historical_odds_events hoe
		LEFT JOIN historical_odds_fights hof ON hof.historical_event_id = hoe.id
		LEFT JOIN historical_prop_odds hpo ON hpo.historical_fight_id = hof.id
		WHERE hoe.source = 'fightodds'
		GROUP BY
			hoe.source_event_id,
			hoe.raw_name,
			hoe.event_date,
			hoe.canonical_event_id
		HAVING count(hpo.id) > 0
		ORDER BY hoe.event_date, hoe.source_event_id
	`) as PropEventCoverage[];
	const outcomes = (await sql`
		SELECT
			outcome_side,
			is_not,
			raw_outcome_name,
			count(*)::int AS rows
		FROM historical_prop_odds
		WHERE source_offer_type_id = 'DISTANCE'
		GROUP BY outcome_side, is_not, raw_outcome_name
		ORDER BY outcome_side, is_not, rows DESC, raw_outcome_name
	`) as OutcomeCoverage[];
	const sourceFights = sum(events, 'source_fights');
	const matchedFights = sum(events, 'matched_fights');
	const propRows = sum(events, 'prop_rows');
	const linkedPropRows = sum(events, 'linked_prop_rows');
	const summary = {
		source_events: events.length,
		source_fights: sourceFights,
		matched_fights: matchedFights,
		distance_markets: sum(events, 'distance_markets'),
		prop_rows: propRows,
		linked_prop_rows: linkedPropRows,
		source_current_rows: sum(events, 'source_current_rows'),
		source_previous_rows: sum(events, 'source_previous_rows'),
		fight_match_rate: ratio(matchedFights, sourceFights),
		prop_link_rate: ratio(linkedPropRows, propRows),
		decision_finish_baselines_ready: propRows > 0 && linkedPropRows === propRows,
	};
	return {
		generated_at: new Date().toISOString(),
		report: 'fightodds-prop-coverage',
		report_only: true,
		writes_model_versions: false,
		summary,
		timestamp_limitations: [
			'Imported prop rows use line_kind source_current or source_previous only.',
			'FightOdds exposes oddsPrev but no previous-price timestamp in this query shape.',
			'oddsOpen, oddsBest, and oddsWorst are preserved in raw_metadata but are not treated as model-ready timestamps.',
		],
		readiness_notes: readinessNotes(summary),
		events,
		outcomes,
	};
}

function renderMarkdown(report: PropCoverageReport): string {
	const lines = [
		'# FightOdds Prop Coverage',
		'',
		`- Generated: \`${report.generated_at}\``,
		`- Report only: \`${report.report_only}\``,
		`- Writes \`model_versions\`: \`${report.writes_model_versions}\``,
		`- Source events with prop rows: ${report.summary.source_events}`,
		`- Fights matched: ${report.summary.matched_fights}/${report.summary.source_fights} (${formatPct(report.summary.fight_match_rate)})`,
		`- Distance markets: ${report.summary.distance_markets}`,
		`- Prop rows linked: ${report.summary.linked_prop_rows}/${report.summary.prop_rows} (${formatPct(report.summary.prop_link_rate)})`,
		`- Current/previous rows: ${report.summary.source_current_rows}/${report.summary.source_previous_rows}`,
		`- Decision/finish baselines ready: \`${report.summary.decision_finish_baselines_ready}\``,
		'',
		'## Readiness',
		'',
		...report.readiness_notes.map((note) => `- ${note}`),
		'',
		'## Timestamp Limits',
		'',
		...report.timestamp_limitations.map((note) => `- ${note}`),
		'',
		'## Events',
		'',
		'| Source event | Date | Fights matched | Distance markets | Prop rows linked |',
		'| --- | --- | ---: | ---: | ---: |',
		...report.events.map(
			(event) =>
				`| ${event.raw_name} (${event.source_event_id}) | ${event.event_date} | ${event.matched_fights}/${event.source_fights} | ${event.distance_markets} | ${event.linked_prop_rows}/${event.prop_rows} |`,
		),
		'',
		'## Outcomes',
		'',
		'| Side | Is not | Outcome | Rows |',
		'| --- | --- | --- | ---: |',
		...report.outcomes.map(
			(outcome) =>
				`| ${outcome.outcome_side} | ${outcome.is_not} | ${outcome.raw_outcome_name} | ${outcome.rows} |`,
		),
	];
	return lines.join('\n');
}

function readinessNotes(summary: PropCoverageReport['summary']): string[] {
	if (!summary.decision_finish_baselines_ready) {
		return [
			'Not ready: imported prop rows are missing, or some rows are not linked to canonical fights.',
		];
	}
	return [
		'Ready for report-only opportunity-harness evaluation of fight_goes_decision and finish_likelihood baselines.',
		'Not ready for betting recommendations or model promotion; the corpus is still a one-event prop slice.',
		'Fighter-specific decision, KO/TKO, submission, and inside-distance method markets are present in source data but remain outside this first imported slice.',
	];
}

function readArg(args: string[], name: string): string | null {
	const index = args.indexOf(name);
	if (index === -1) {
		return null;
	}
	const value = args[index + 1];
	if (!value || value.startsWith('--')) {
		throw new Error(`${name} requires a value`);
	}
	return value;
}

function resolveRepoPath(path: string): string {
	return resolve(REPO_ROOT, path);
}

function displayPath(path: string): string {
	return relativePath(REPO_ROOT, path);
}

function relativePath(from: string, to: string): string {
	return to.startsWith(from) ? to.slice(from.length + 1) : to;
}

function sum<T extends Record<string, unknown>>(rows: T[], key: keyof T): number {
	return rows.reduce((total, row) => total + Number(row[key]), 0);
}

function ratio(numerator: number, denominator: number): number | null {
	return denominator === 0 ? null : numerator / denominator;
}

function formatPct(value: number | null): string {
	if (value === null) return 'n/a';
	return `${(value * 100).toFixed(1)}%`;
}

if (process.argv[1]?.endsWith('report-fightodds-props.ts')) {
	main().catch((error) => {
		console.error(error instanceof Error ? error.message : error);
		process.exit(1);
	});
}
