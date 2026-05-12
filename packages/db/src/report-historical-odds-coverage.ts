import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, relative, resolve } from 'node:path';
import { sql } from './client.js';

const REPO_ROOT = resolve(import.meta.dirname, '../../..');
const DEFAULT_JSON_OUTPUT = 'data/experiments/historical-odds-coverage.json';
const DEFAULT_MARKDOWN_OUTPUT = 'data/experiments/historical-odds-coverage.md';

type CoverageEvent = {
	source_event_id: string;
	raw_name: string;
	event_date: string;
	canonical_event_id: string | null;
	match_status: string;
	source_fights: number;
	matched_fights: number;
	ambiguous_fights: number;
	unmatched_fights: number;
	cancelled_unmatched_fights: number;
	moneyline_rows: number;
	linked_moneyline_rows: number;
	review_rows: number;
};

type CoverageReport = {
	generated_at: string;
	report: 'historical-odds-coverage';
	report_only: true;
	writes_model_versions: false;
	summary: {
		source_events: number;
		matched_source_events: number;
		source_fights: number;
		matched_fights: number;
		ambiguous_fights: number;
		unmatched_fights: number;
		cancelled_unmatched_fights: number;
		moneyline_rows: number;
		linked_moneyline_rows: number;
		review_rows: number;
		fight_match_rate: number | null;
		moneyline_link_rate: number | null;
	};
	events: CoverageEvent[];
};

async function main() {
	const output = resolveRepoPath(readArg(process.argv.slice(2), '--output') ?? DEFAULT_JSON_OUTPUT);
	const markdown = resolveRepoPath(
		readArg(process.argv.slice(2), '--markdown') ?? DEFAULT_MARKDOWN_OUTPUT,
	);
	try {
		const report = await buildCoverageReport();
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

export async function buildCoverageReport(): Promise<CoverageReport> {
	const events = (await sql`
		SELECT
			hoe.source_event_id,
			hoe.raw_name,
			hoe.event_date::text AS event_date,
			hoe.canonical_event_id,
			hoe.match_status,
			count(DISTINCT hof.id)::int AS source_fights,
			count(DISTINCT hof.id) FILTER (WHERE hof.match_status = 'matched')::int AS matched_fights,
			count(DISTINCT hof.id) FILTER (WHERE hof.match_status = 'ambiguous')::int AS ambiguous_fights,
			count(DISTINCT hof.id) FILTER (WHERE hof.match_status = 'unmatched')::int AS unmatched_fights,
			count(DISTINCT hof.id) FILTER (
				WHERE hof.match_status != 'matched' AND hof.is_cancelled = true
			)::int AS cancelled_unmatched_fights,
			count(DISTINCT hmo.id)::int AS moneyline_rows,
			count(DISTINCT hmo.id) FILTER (WHERE hmo.canonical_fighter_id IS NOT NULL)::int AS linked_moneyline_rows,
			count(DISTINCT uho.id)::int AS review_rows
		FROM historical_odds_events hoe
		LEFT JOIN historical_odds_fights hof ON hof.historical_event_id = hoe.id
		LEFT JOIN historical_moneyline_odds hmo ON hmo.historical_fight_id = hof.id
		LEFT JOIN unmatched_historical_odds uho
			ON uho.source_event_id = hoe.source_event_id
			AND uho.source_fight_id = hof.source_fight_id
		WHERE hoe.source = 'fightodds'
		GROUP BY
			hoe.source_event_id,
			hoe.raw_name,
			hoe.event_date,
			hoe.canonical_event_id,
			hoe.match_status
		ORDER BY hoe.event_date, hoe.source_event_id
	`) as CoverageEvent[];
	const summary = {
		source_events: events.length,
		matched_source_events: events.filter((event) => event.canonical_event_id !== null).length,
		source_fights: sum(events, 'source_fights'),
		matched_fights: sum(events, 'matched_fights'),
		ambiguous_fights: sum(events, 'ambiguous_fights'),
		unmatched_fights: sum(events, 'unmatched_fights'),
		cancelled_unmatched_fights: sum(events, 'cancelled_unmatched_fights'),
		moneyline_rows: sum(events, 'moneyline_rows'),
		linked_moneyline_rows: sum(events, 'linked_moneyline_rows'),
		review_rows: sum(events, 'review_rows'),
		fight_match_rate: ratio(sum(events, 'matched_fights'), sum(events, 'source_fights')),
		moneyline_link_rate: ratio(sum(events, 'linked_moneyline_rows'), sum(events, 'moneyline_rows')),
	};
	return {
		generated_at: new Date().toISOString(),
		report: 'historical-odds-coverage',
		report_only: true,
		writes_model_versions: false,
		summary,
		events,
	};
}

function renderMarkdown(report: CoverageReport): string {
	const lines = [
		'# Historical Odds Coverage',
		'',
		`- Generated: \`${report.generated_at}\``,
		`- Source events: ${report.summary.matched_source_events}/${report.summary.source_events} matched`,
		`- Fights matched: ${report.summary.matched_fights}/${report.summary.source_fights} (${formatPct(report.summary.fight_match_rate)})`,
		`- Moneyline rows linked: ${report.summary.linked_moneyline_rows}/${report.summary.moneyline_rows} (${formatPct(report.summary.moneyline_link_rate)})`,
		`- Review rows: ${report.summary.review_rows}`,
		`- Writes \`model_versions\`: \`${report.writes_model_versions}\``,
		'',
		'## Events',
		'',
		'| Source event | Canonical event | Date | Status | Fights | Moneylines | Review rows |',
		'|---|---|---:|---|---:|---:|---:|',
	];
	for (const event of report.events) {
		lines.push(
			`| ${event.source_event_id} ${escapeMd(event.raw_name)} | ${event.canonical_event_id ?? ''} | ${event.event_date} | ${event.match_status} | ${event.matched_fights}/${event.source_fights} | ${event.linked_moneyline_rows}/${event.moneyline_rows} | ${event.review_rows} |`,
		);
	}
	lines.push(
		'',
		'Unmatched and ambiguous fights remain reviewable in `unmatched_historical_odds`; they are not silently dropped.',
	);
	return lines.join('\n');
}

function readArg(args: string[], name: string): string | null {
	const index = args.indexOf(name);
	if (index === -1) return null;
	const value = args[index + 1];
	if (!value || value.startsWith('--')) throw new Error(`${name} requires a value`);
	return value;
}

function resolveRepoPath(path: string): string {
	return resolve(REPO_ROOT, path);
}

function displayPath(path: string): string {
	return relative(REPO_ROOT, path);
}

function sum(events: CoverageEvent[], key: keyof CoverageEvent): number {
	return events.reduce((total, event) => total + Number(event[key] ?? 0), 0);
}

function ratio(numerator: number, denominator: number): number | null {
	return denominator === 0 ? null : numerator / denominator;
}

function formatPct(value: number | null): string {
	return value === null ? '' : `${(value * 100).toFixed(1)}%`;
}

function escapeMd(value: string): string {
	return value.replace(/\|/g, '\\|');
}

if (process.argv[1]?.endsWith('report-historical-odds-coverage.ts')) {
	main().catch((error) => {
		console.error(error instanceof Error ? error.message : error);
		process.exit(1);
	});
}
