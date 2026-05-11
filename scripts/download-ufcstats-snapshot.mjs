#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const REPO_OWNER = 'Greco1899';
const REPO_NAME = 'scrape_ufc_stats';
const SOURCE_REPO_URL = `https://github.com/${REPO_OWNER}/${REPO_NAME}`;
const DEFAULT_REF = 'main';
const DEFAULT_OUTPUT_ROOT = 'data/external/ufcstats';
const REQUIRED_FILES = [
	'ufc_event_details.csv',
	'ufc_fight_details.csv',
	'ufc_fight_results.csv',
	'ufc_fight_stats.csv',
	'ufc_fighter_details.csv',
	'ufc_fighter_tott.csv',
];

function usage() {
	console.log(`Usage: pnpm data:ufcstats:snapshot [-- --ref main] [-- --out-dir data/external/ufcstats] [-- --snapshot-id <id>]

Downloads the six published CSV files from ${SOURCE_REPO_URL}.
The default output path is ignored by git: ${DEFAULT_OUTPUT_ROOT}/<snapshot-id>/`);
}

function parseArgs(argv) {
	const options = {
		ref: process.env.UFCSTATS_SOURCE_REF || DEFAULT_REF,
		outputRoot: process.env.UFCSTATS_OUTPUT_ROOT || DEFAULT_OUTPUT_ROOT,
		snapshotId: process.env.UFCSTATS_SNAPSHOT_ID || undefined,
	};

	for (let index = 0; index < argv.length; index += 1) {
		const arg = argv[index];
		if (arg === '--') {
			continue;
		}
		if (arg === '--help' || arg === '-h') {
			usage();
			process.exit(0);
		}
		if (arg === '--ref') {
			options.ref = readValue(argv, index, arg);
			index += 1;
			continue;
		}
		if (arg === '--out-dir') {
			options.outputRoot = readValue(argv, index, arg);
			index += 1;
			continue;
		}
		if (arg === '--snapshot-id') {
			options.snapshotId = readValue(argv, index, arg);
			index += 1;
			continue;
		}
		throw new Error(`Unknown argument: ${arg}`);
	}

	return options;
}

function readValue(argv, index, arg) {
	const value = argv[index + 1];
	if (!value || value.startsWith('--')) {
		throw new Error(`${arg} requires a value`);
	}
	return value;
}

function githubHeaders() {
	const headers = {
		'User-Agent': 'interceptor-ufcstats-snapshot-downloader',
		Accept: 'application/vnd.github+json',
		'X-GitHub-Api-Version': '2022-11-28',
	};

	if (process.env.GITHUB_TOKEN) {
		headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
	}

	return headers;
}

async function resolveCommitSha(ref) {
	const url = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits/${encodeURIComponent(ref)}`;
	const response = await fetch(url, { headers: githubHeaders() });

	if (!response.ok) {
		throw new Error(
			`Failed to resolve ${ref} from GitHub API: ${response.status} ${response.statusText}`,
		);
	}

	const payload = await response.json();
	if (typeof payload.sha !== 'string' || payload.sha.length === 0) {
		throw new Error(`GitHub API response for ${ref} did not include a commit SHA`);
	}

	return payload.sha;
}

function rawUrl(refOrSha, fileName) {
	return `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${encodeURIComponent(refOrSha)}/${fileName}`;
}

function snapshotTimestamp(date) {
	return date
		.toISOString()
		.replaceAll('-', '')
		.replaceAll(':', '')
		.replace(/\.\d{3}Z$/, 'Z');
}

function sanitizeSegment(value) {
	return value.replace(/[^a-zA-Z0-9._-]/g, '-');
}

function validateSnapshotId(value) {
	if (!/^[a-zA-Z0-9._-]+$/.test(value)) {
		throw new Error('Snapshot ID may contain only letters, numbers, dots, underscores, and dashes');
	}
}

async function downloadFile(url) {
	const response = await fetch(url, {
		headers: {
			'User-Agent': 'interceptor-ufcstats-snapshot-downloader',
			Accept: 'text/csv,text/plain,*/*',
		},
	});

	if (!response.ok) {
		throw new Error(`Failed to download ${url}: ${response.status} ${response.statusText}`);
	}

	const bytes = Buffer.from(await response.arrayBuffer());
	return {
		bytes,
		metadata: {
			url,
			status: response.status,
			etag: response.headers.get('etag'),
			lastModified: response.headers.get('last-modified'),
			contentType: response.headers.get('content-type'),
			sizeBytes: bytes.byteLength,
			sha256: createHash('sha256').update(bytes).digest('hex'),
		},
	};
}

async function main() {
	const options = parseArgs(process.argv.slice(2));
	const retrievedAt = new Date();
	const commitSha = await resolveCommitSha(options.ref);
	const snapshotId =
		options.snapshotId ||
		`${snapshotTimestamp(retrievedAt)}-${sanitizeSegment(commitSha.slice(0, 12))}`;
	validateSnapshotId(snapshotId);
	const snapshotDir = path.join(options.outputRoot, snapshotId);

	await mkdir(snapshotDir, { recursive: true });

	const files = [];
	for (const fileName of REQUIRED_FILES) {
		const url = rawUrl(commitSha, fileName);
		const { bytes, metadata } = await downloadFile(url);
		const outputPath = path.join(snapshotDir, fileName);
		await writeFile(outputPath, bytes);
		files.push({
			fileName,
			path: outputPath,
			...metadata,
		});
		console.log(`downloaded ${fileName} (${metadata.sizeBytes} bytes)`);
	}

	const metadata = {
		snapshotId,
		retrievedAt: retrievedAt.toISOString(),
		source: {
			repoUrl: SOURCE_REPO_URL,
			branchOrRef: options.ref,
			resolvedCommitSha: commitSha,
			apiCommitUrl: `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits/${encodeURIComponent(options.ref)}`,
			rawBaseUrl: `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${commitSha}/`,
		},
		license: {
			upstreamLicense: 'GPL-3.0',
			note: 'CSV files are downloaded as external local data for model research. This repository does not vendor upstream scraper code, notebooks, or library files.',
		},
		files,
	};

	const metadataPath = path.join(snapshotDir, 'metadata.json');
	await writeFile(metadataPath, `${JSON.stringify(metadata, null, 2)}\n`);
	console.log(`metadata ${metadataPath}`);
	console.log(`snapshot ${snapshotDir}`);
}

main().catch((error) => {
	console.error(error instanceof Error ? error.message : error);
	process.exit(1);
});
