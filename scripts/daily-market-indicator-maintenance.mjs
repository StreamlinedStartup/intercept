#!/usr/bin/env node
import { spawn } from 'node:child_process';

const DEFAULT_API_BASE_URL = 'http://localhost:3001';

const args = new Set(process.argv.slice(2));
const dryRun = args.has('--dry-run');
const apiBaseUrl = valueArg('--api-base-url') ?? process.env.API_BASE_URL ?? DEFAULT_API_BASE_URL;
const eventPks = valueArg('--fightodds-event-pks') ?? process.env.FIGHTODDS_EVENT_PKS ?? '';

const steps = [
	{
		name: 'sync_upcoming_cards',
		description: 'Sync upcoming UFCStats cards into canonical events/fights/fight_results.',
		run: () => postJson('/api/predict/sync/upcoming-cards'),
	},
	{
		name: 'refresh_upcoming_backfill',
		description: 'Queue 30-day upcoming fighter backfill refreshes.',
		run: () => postJson('/api/predict/backfill/seed?scope=in-window'),
	},
	{
		name: 'import_moneylines',
		description: 'Snapshot current MMA moneylines from odds-mma.',
		run: () => getJson('/api/odds-mma/snapshot?refresh=1'),
	},
	{
		name: 'import_props',
		description: 'Import FightOdds event props when FIGHTODDS_EVENT_PKS is set.',
		run: () =>
			eventPks.trim()
				? runCommand('pnpm', [
						'--filter',
						'@interceptor/db',
						'import:fightodds:event',
						'--',
						'--event-pks',
						eventPks,
						'--include-props',
					])
				: skipped('FIGHTODDS_EVENT_PKS is not set; props import requires explicit event ids.'),
	},
	{
		name: 'canonical_match_odds',
		description: 'Canonical-match imported FightOdds rows.',
		run: () =>
			eventPks.trim()
				? runCommand('pnpm', ['--filter', '@interceptor/db', 'match:fightodds:all'])
				: skipped(
						'FIGHTODDS_EVENT_PKS is not set; canonical prop matching skipped with props import.',
					),
	},
	{
		name: 'refresh_indicator_snapshots',
		description: 'Refresh report-only materialized market indicator snapshots.',
		run: () => runCommand('pnpm', ['--filter', '@interceptor/db', 'refresh:market-indicators']),
	},
];

const startedAt = new Date().toISOString();
const results = [];
let status = 'completed';

for (const step of steps) {
	const stepStartedAt = new Date().toISOString();
	try {
		const result = dryRun ? { status: 'dry_run', detail: step.description } : await step.run();
		results.push({ name: step.name, started_at: stepStartedAt, ...result });
		if (result.status === 'failed') {
			status = 'failed';
			break;
		}
	} catch (error) {
		status = 'failed';
		results.push({
			name: step.name,
			started_at: stepStartedAt,
			status: 'failed',
			error: error instanceof Error ? error.message : String(error),
		});
		break;
	}
}

const summary = {
	job: 'daily-market-indicator-maintenance',
	status,
	dry_run: dryRun,
	started_at: startedAt,
	completed_at: new Date().toISOString(),
	policy: 'report_only_no_retraining_no_artifact_promotion',
	api_base_url: apiBaseUrl,
	steps: results,
};

console.log(JSON.stringify(summary, null, 2));
if (status !== 'completed') process.exit(1);

function valueArg(name) {
	const prefix = `${name}=`;
	const arg = process.argv.slice(2).find((value) => value.startsWith(prefix));
	return arg ? arg.slice(prefix.length) : null;
}

async function postJson(path) {
	return fetchJson(path, { method: 'POST' });
}

async function getJson(path) {
	return fetchJson(path, { method: 'GET' });
}

async function fetchJson(path, init) {
	const url = `${apiBaseUrl}${path}`;
	const response = await fetch(url, init);
	const text = await response.text();
	const body = parseBody(text);
	if (!response.ok) {
		return {
			status: 'failed',
			http_status: response.status,
			url,
			body,
		};
	}
	return {
		status: 'completed',
		http_status: response.status,
		url,
		body,
	};
}

function parseBody(text) {
	if (!text) return null;
	try {
		return JSON.parse(text);
	} catch {
		return text;
	}
}

function runCommand(command, commandArgs) {
	return new Promise((resolve) => {
		const child = spawn(command, commandArgs, {
			cwd: process.cwd(),
			env: process.env,
			stdio: ['ignore', 'pipe', 'pipe'],
		});
		let stdout = '';
		let stderr = '';
		child.stdout.on('data', (chunk) => {
			stdout += chunk.toString();
		});
		child.stderr.on('data', (chunk) => {
			stderr += chunk.toString();
		});
		child.on('close', (code) => {
			const result = {
				status: code === 0 ? 'completed' : 'failed',
				command: [command, ...commandArgs].join(' '),
				exit_code: code,
				stdout: stdout.trim(),
				stderr: stderr.trim(),
			};
			resolve(result);
		});
	});
}

function skipped(reason) {
	return {
		status: 'skipped',
		reason,
	};
}
