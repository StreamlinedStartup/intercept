import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { db, sql } from './client.js';
import {
	events,
	fighterBackfillState,
	fighters,
	fightResults,
	fightRoundStats,
	fights,
} from './schema.js';

const REQUIRED_FILES = {
	events: 'ufc_event_details.csv',
	fightDetails: 'ufc_fight_details.csv',
	fightResults: 'ufc_fight_results.csv',
	fightStats: 'ufc_fight_stats.csv',
	fighterDetails: 'ufc_fighter_details.csv',
	fighterTott: 'ufc_fighter_tott.csv',
} as const;

type CsvRow = Record<string, string>;

type FighterImport = {
	id: string;
	name: string;
	nickname: string | null;
	dob: string | null;
	heightIn: number | null;
	reachIn: number | null;
	stance: string | null;
	weightLbs: number | null;
	aliases: string[];
	historyCount: number;
};

type FightImport = {
	id: string;
	eventId: string;
	weightClass: string | null;
	scheduledRounds: number | null;
	isHeadliner: boolean;
};

type ResultImport = {
	fightId: string;
	fighterId: string;
	opponentId: string;
	outcome: 'win' | 'loss' | 'draw' | 'nc';
	method: string | null;
	methodDetail: string | null;
	round: number | null;
	timeSeconds: number | null;
	knockdowns: number | null;
	sigStrikesLanded: number | null;
	sigStrikesAttempted: number | null;
	totalStrikesLanded: number | null;
	totalStrikesAttempted: number | null;
	takedownsLanded: number | null;
	takedownsAttempted: number | null;
	subAttempts: number | null;
	ctrlSeconds: number | null;
	reversals: number | null;
};

type RoundStatImport = Omit<
	ResultImport,
	'opponentId' | 'outcome' | 'method' | 'methodDetail' | 'timeSeconds'
> & {
	round: number;
};

type FighterStateImport = {
	fighterId: string;
	historyCountAtBackfill: number;
	lastKnownFightId: string | null;
};

type ImportSummary = {
	snapshotDir: string;
	sourceCommitSha: string | null;
	events: number;
	fighters: number;
	fights: number;
	fightResults: number;
	fightRoundStats: number;
	fighterBackfillState: number;
	skippedFightRows: number;
	skippedFightStatsRows: number;
};

function usage() {
	console.log(`Usage: pnpm --filter @interceptor/db import:ufcstats <snapshot-dir>

Imports an ignored external UFC Stats CSV snapshot into the canonical predictor tables.
Example: pnpm --filter @interceptor/db import:ufcstats data/external/ufcstats/codex-verify-n89z-2`);
}

async function main() {
	const snapshotDir = process.argv[2];
	if (!snapshotDir || snapshotDir === '--help' || snapshotDir === '-h') {
		usage();
		process.exit(snapshotDir ? 0 : 1);
	}

	const summary = await importSnapshot(snapshotDir);
	console.log(JSON.stringify(summary, null, 2));
}

async function importSnapshot(snapshotDir: string): Promise<ImportSummary> {
	const absoluteDir = path.resolve(process.env.INIT_CWD ?? process.cwd(), snapshotDir);
	const [
		metadata,
		eventRows,
		fightDetailRows,
		fightResultRows,
		fightStatRows,
		fighterDetailRows,
		tottRows,
	] = await Promise.all([
		readMetadata(absoluteDir),
		readCsvFile(absoluteDir, REQUIRED_FILES.events, ['EVENT', 'URL', 'DATE', 'LOCATION']),
		readCsvFile(absoluteDir, REQUIRED_FILES.fightDetails, ['EVENT', 'BOUT', 'URL']),
		readCsvFile(absoluteDir, REQUIRED_FILES.fightResults, [
			'EVENT',
			'BOUT',
			'OUTCOME',
			'WEIGHTCLASS',
			'METHOD',
			'ROUND',
			'TIME',
			'TIME FORMAT',
			'DETAILS',
			'URL',
		]),
		readCsvFile(absoluteDir, REQUIRED_FILES.fightStats, [
			'EVENT',
			'BOUT',
			'ROUND',
			'FIGHTER',
			'KD',
			'SIG.STR.',
			'TOTAL STR.',
			'TD',
			'SUB.ATT',
			'REV.',
			'CTRL',
		]),
		readCsvFile(absoluteDir, REQUIRED_FILES.fighterDetails, ['FIRST', 'LAST', 'NICKNAME', 'URL']),
		readCsvFile(absoluteDir, REQUIRED_FILES.fighterTott, [
			'FIGHTER',
			'HEIGHT',
			'REACH',
			'STANCE',
			'DOB',
			'URL',
		]),
	]);

	validateMetadata(metadata, absoluteDir);

	const eventImports = buildEvents(eventRows);
	const fightersById = buildFighters(fighterDetailRows, tottRows);
	const nameIndex = buildNameIndex(fightersById);
	const fightUrlsByKey = buildFightUrlIndex(fightDetailRows);
	const fightImports = new Map<string, FightImport>();
	const resultImports = new Map<string, ResultImport>();
	const roundImports = new Map<string, RoundStatImport>();
	const fighterFightIds = new Map<string, Set<string>>();
	const fighterLastFight = new Map<string, { fightId: string; eventDate: string }>();
	let skippedFightRows = 0;
	let skippedFightStatsRows = 0;

	for (let index = 0; index < fightResultRows.length; index += 1) {
		const row = fightResultRows[index];
		const fightId = extractUfcstatsId(row.URL || onlyFightUrl(fightUrlsByKey, row.EVENT, row.BOUT));
		const event = eventImports.get(normalizeText(row.EVENT));
		if (!fightId || !event) {
			throw new Error(`Cannot map fight result row ${index + 2} to a fight and event`);
		}

		let fighterAId: string;
		let fighterBId: string;
		try {
			const boutFighters = parseBout(row.BOUT);
			fighterAId = resolveFighterId(
				nameIndex,
				fightersById,
				boutFighters[0],
				`fight result row ${index + 2}`,
				row.WEIGHTCLASS,
			);
			fighterBId = resolveFighterId(
				nameIndex,
				fightersById,
				boutFighters[1],
				`fight result row ${index + 2}`,
				row.WEIGHTCLASS,
			);
		} catch (error) {
			skippedFightRows += 1;
			console.warn(error instanceof Error ? `skipped ${error.message}` : error);
			continue;
		}
		const outcomes = parseOutcomes(row.OUTCOME);
		const finishRound = parseInteger(row.ROUND);

		fightImports.set(fightId, {
			id: fightId,
			eventId: event.id,
			weightClass: normalizeWeightClass(row.WEIGHTCLASS),
			scheduledRounds: parseScheduledRounds(row['TIME FORMAT']),
			isHeadliner: index === 0 || eventFirstFightId(fightImports, event.id) === null,
		});

		const finishSeconds = parseFightElapsedSeconds(finishRound, row.TIME);
		const base = {
			fightId,
			method: clean(row.METHOD),
			methodDetail: clean(row.DETAILS),
			round: finishRound,
			timeSeconds: finishSeconds,
			knockdowns: null,
			sigStrikesLanded: null,
			sigStrikesAttempted: null,
			totalStrikesLanded: null,
			totalStrikesAttempted: null,
			takedownsLanded: null,
			takedownsAttempted: null,
			subAttempts: null,
			ctrlSeconds: null,
			reversals: null,
		};

		resultImports.set(resultKey(fightId, fighterAId), {
			...base,
			fighterId: fighterAId,
			opponentId: fighterBId,
			outcome: outcomes[0],
		});
		resultImports.set(resultKey(fightId, fighterBId), {
			...base,
			fighterId: fighterBId,
			opponentId: fighterAId,
			outcome: outcomes[1],
		});

		rememberFight(fighterFightIds, fighterLastFight, fighterAId, fightId, event.date);
		rememberFight(fighterFightIds, fighterLastFight, fighterBId, fightId, event.date);
	}

	for (let index = 0; index < fightStatRows.length; index += 1) {
		const row = fightStatRows[index];
		if (!clean(row.ROUND) && !clean(row.FIGHTER)) {
			skippedFightStatsRows += 1;
			continue;
		}

		const urls = fightUrlsByKey.get(fightKey(row.EVENT, row.BOUT)) ?? [];
		if (urls.length !== 1) {
			skippedFightStatsRows += 1;
			continue;
		}

		const fightId = extractUfcstatsId(urls[0]);
		if (!fightId) {
			throw new Error(`Cannot map fight stats row ${index + 2} to a fight URL`);
		}
		if (![...resultImports.values()].some((result) => result.fightId === fightId)) {
			skippedFightStatsRows += 1;
			continue;
		}

		let fighterId: string;
		try {
			fighterId = resolveFightStatFighterId(
				resultImports,
				fightersById,
				fightId,
				row.FIGHTER,
				`fight stats row ${index + 2}`,
			);
		} catch (error) {
			skippedFightStatsRows += 1;
			console.warn(error instanceof Error ? `skipped ${error.message}` : error);
			continue;
		}
		const round = parseRound(row.ROUND);
		if (!round) {
			throw new Error(`Cannot parse round in fight stats row ${index + 2}: ${row.ROUND}`);
		}

		const parsedStats = parseStats(row);
		roundImports.set(roundKey(fightId, fighterId, round), {
			fightId,
			fighterId,
			round,
			...parsedStats,
		});

		const existing = resultImports.get(resultKey(fightId, fighterId));
		if (existing) {
			resultImports.set(resultKey(fightId, fighterId), addStats(existing, parsedStats));
		}
	}

	const fighterStates: FighterStateImport[] = [];
	for (const [fighterId, fightIds] of fighterFightIds) {
		const fighter = fightersById.get(fighterId);
		if (fighter) {
			fighter.historyCount = fightIds.size;
		}
		fighterStates.push({
			fighterId,
			historyCountAtBackfill: fightIds.size,
			lastKnownFightId: fighterLastFight.get(fighterId)?.fightId ?? null,
		});
	}

	await db.transaction(async (tx) => {
		for (const event of eventImports.values()) {
			await tx.insert(events).values(event).onConflictDoUpdate({
				target: events.id,
				set: event,
			});
		}

		for (const fighter of fightersById.values()) {
			await tx
				.insert(fighters)
				.values(fighter)
				.onConflictDoUpdate({
					target: fighters.id,
					set: {
						name: fighter.name,
						nickname: fighter.nickname,
						dob: fighter.dob,
						heightIn: fighter.heightIn,
						reachIn: fighter.reachIn,
						stance: fighter.stance,
						historyCount: fighter.historyCount,
					},
				});
		}

		for (const fight of fightImports.values()) {
			await tx
				.insert(fights)
				.values(fight)
				.onConflictDoUpdate({
					target: fights.id,
					set: {
						eventId: fight.eventId,
						weightClass: fight.weightClass,
						scheduledRounds: fight.scheduledRounds,
						isHeadliner: fight.isHeadliner,
					},
				});
		}

		for (const result of resultImports.values()) {
			await tx
				.insert(fightResults)
				.values(result)
				.onConflictDoUpdate({
					target: [fightResults.fightId, fightResults.fighterId],
					set: {
						opponentId: result.opponentId,
						outcome: result.outcome,
						method: result.method,
						methodDetail: result.methodDetail,
						round: result.round,
						timeSeconds: result.timeSeconds,
						knockdowns: result.knockdowns,
						sigStrikesLanded: result.sigStrikesLanded,
						sigStrikesAttempted: result.sigStrikesAttempted,
						totalStrikesLanded: result.totalStrikesLanded,
						totalStrikesAttempted: result.totalStrikesAttempted,
						takedownsLanded: result.takedownsLanded,
						takedownsAttempted: result.takedownsAttempted,
						subAttempts: result.subAttempts,
						ctrlSeconds: result.ctrlSeconds,
						reversals: result.reversals,
					},
				});
		}

		for (const roundStat of roundImports.values()) {
			await tx
				.insert(fightRoundStats)
				.values(roundStat)
				.onConflictDoUpdate({
					target: [fightRoundStats.fightId, fightRoundStats.fighterId, fightRoundStats.round],
					set: {
						knockdowns: roundStat.knockdowns,
						sigStrikesLanded: roundStat.sigStrikesLanded,
						sigStrikesAttempted: roundStat.sigStrikesAttempted,
						totalStrikesLanded: roundStat.totalStrikesLanded,
						totalStrikesAttempted: roundStat.totalStrikesAttempted,
						takedownsLanded: roundStat.takedownsLanded,
						takedownsAttempted: roundStat.takedownsAttempted,
						subAttempts: roundStat.subAttempts,
						ctrlSeconds: roundStat.ctrlSeconds,
						reversals: roundStat.reversals,
					},
				});
		}

		for (const state of fighterStates) {
			await tx
				.insert(fighterBackfillState)
				.values({
					fighterId: state.fighterId,
					lastBackfilledAt: new Date(),
					historyCountAtBackfill: state.historyCountAtBackfill,
					lastKnownFightId: state.lastKnownFightId,
					status: 'current',
					lastError: null,
				})
				.onConflictDoUpdate({
					target: fighterBackfillState.fighterId,
					set: {
						lastBackfilledAt: new Date(),
						historyCountAtBackfill: state.historyCountAtBackfill,
						lastKnownFightId: state.lastKnownFightId,
						status: 'current',
						lastError: null,
					},
				});
		}
	});

	await sql.end();

	return {
		snapshotDir: absoluteDir,
		sourceCommitSha: metadata.sourceCommitSha,
		events: eventImports.size,
		fighters: fightersById.size,
		fights: fightImports.size,
		fightResults: resultImports.size,
		fightRoundStats: roundImports.size,
		fighterBackfillState: fighterStates.length,
		skippedFightRows,
		skippedFightStatsRows,
	};
}

async function readMetadata(snapshotDir: string): Promise<{ sourceCommitSha: string | null }> {
	const metadataPath = path.join(snapshotDir, 'metadata.json');
	const text = await readFile(metadataPath, 'utf8');
	const parsed = JSON.parse(text) as {
		source?: { resolvedCommitSha?: unknown };
		files?: Array<{ fileName?: unknown; sha256?: unknown }>;
	};

	for (const file of parsed.files ?? []) {
		if (typeof file.fileName !== 'string' || typeof file.sha256 !== 'string') continue;
		const bytes = await readFile(path.join(snapshotDir, file.fileName));
		const sha256 = createHash('sha256').update(bytes).digest('hex');
		if (sha256 !== file.sha256) {
			throw new Error(`Snapshot hash mismatch for ${file.fileName}`);
		}
	}

	return {
		sourceCommitSha:
			typeof parsed.source?.resolvedCommitSha === 'string' ? parsed.source.resolvedCommitSha : null,
	};
}

function validateMetadata(metadata: { sourceCommitSha: string | null }, snapshotDir: string) {
	if (!metadata.sourceCommitSha) {
		throw new Error(`Snapshot metadata at ${snapshotDir} is missing source.resolvedCommitSha`);
	}
}

async function readCsvFile(
	snapshotDir: string,
	fileName: string,
	requiredHeaders: string[],
): Promise<CsvRow[]> {
	const text = await readFile(path.join(snapshotDir, fileName), 'utf8');
	const { headers, rows } = parseCsv(text);
	for (const header of requiredHeaders) {
		if (!headers.includes(header)) {
			throw new Error(`${fileName} is missing required header ${header}`);
		}
	}
	return rows;
}

function parseCsv(text: string): { headers: string[]; rows: CsvRow[] } {
	const records: string[][] = [];
	let field = '';
	let record: string[] = [];
	let quoted = false;

	for (let index = 0; index < text.length; index += 1) {
		const char = text[index];
		const next = text[index + 1];

		if (quoted) {
			if (char === '"' && next === '"') {
				field += '"';
				index += 1;
			} else if (char === '"') {
				quoted = false;
			} else {
				field += char;
			}
			continue;
		}

		if (char === '"') {
			quoted = true;
		} else if (char === ',') {
			record.push(field);
			field = '';
		} else if (char === '\n') {
			record.push(field);
			records.push(record);
			record = [];
			field = '';
		} else if (char !== '\r') {
			field += char;
		}
	}

	if (field.length > 0 || record.length > 0) {
		record.push(field);
		records.push(record);
	}

	const headers = records.shift()?.map((header) => header.trim()) ?? [];
	const rows = records
		.filter((row) => row.some((value) => value.trim() !== ''))
		.map((row, rowIndex) => {
			if (row.length !== headers.length) {
				throw new Error(
					`CSV row ${rowIndex + 2} has ${row.length} fields; expected ${headers.length}`,
				);
			}
			return Object.fromEntries(headers.map((header, index) => [header, row[index] ?? '']));
		});
	return { headers, rows };
}

function buildEvents(rows: CsvRow[]) {
	const mapped = new Map<
		string,
		{
			id: string;
			name: string;
			date: string;
			location: string | null;
			completed: boolean;
			promotion: 'ufc';
		}
	>();
	for (const [index, row] of rows.entries()) {
		const id = extractUfcstatsId(row.URL);
		const date = parseDate(row.DATE);
		if (!id || !date) {
			throw new Error(`Cannot parse event row ${index + 2}`);
		}
		mapped.set(normalizeText(row.EVENT), {
			id,
			name: row.EVENT.trim(),
			date,
			location: clean(row.LOCATION),
			completed: true,
			promotion: 'ufc',
		});
	}
	return mapped;
}

function buildFighters(detailsRows: CsvRow[], tottRows: CsvRow[]) {
	const fightersById = new Map<string, FighterImport>();

	for (const [index, row] of detailsRows.entries()) {
		const id = extractUfcstatsId(row.URL);
		if (!id) {
			throw new Error(`Cannot parse fighter details row ${index + 2}`);
		}
		const name = `${row.FIRST.trim()} ${row.LAST.trim()}`.trim();
		fightersById.set(id, {
			id,
			name,
			nickname: clean(row.NICKNAME),
			dob: null,
			heightIn: null,
			reachIn: null,
			stance: null,
			weightLbs: null,
			aliases: [name],
			historyCount: 0,
		});
	}

	for (const [index, row] of tottRows.entries()) {
		const id = extractUfcstatsId(row.URL);
		if (!id) {
			throw new Error(`Cannot parse fighter tale-of-the-tape row ${index + 2}`);
		}
		const existing = fightersById.get(id);
		const tottName = row.FIGHTER.trim();
		fightersById.set(id, {
			id,
			name: existing?.name || tottName,
			nickname: existing?.nickname ?? null,
			dob: parseDate(row.DOB),
			heightIn: parseHeightInches(row.HEIGHT),
			reachIn: parseReachInches(row.REACH),
			stance: clean(row.STANCE),
			weightLbs: parseWeightPounds(row.WEIGHT),
			aliases: uniqueStrings([...(existing?.aliases ?? []), tottName]),
			historyCount: existing?.historyCount ?? 0,
		});
	}

	return fightersById;
}

function buildNameIndex(fightersById: Map<string, FighterImport>) {
	const index = new Map<string, string[]>();
	for (const fighter of fightersById.values()) {
		for (const alias of fighter.aliases) {
			const key = normalizeName(alias);
			index.set(key, [...(index.get(key) ?? []), fighter.id]);
		}
	}
	return index;
}

function buildFightUrlIndex(rows: CsvRow[]) {
	const index = new Map<string, string[]>();
	for (const row of rows) {
		const key = fightKey(row.EVENT, row.BOUT);
		index.set(key, [...(index.get(key) ?? []), row.URL]);
	}
	return index;
}

function onlyFightUrl(index: Map<string, string[]>, eventName: string, bout: string) {
	const urls = index.get(fightKey(eventName, bout)) ?? [];
	return urls.length === 1 ? urls[0] : undefined;
}

function eventFirstFightId(fightsById: Map<string, FightImport>, eventId: string) {
	for (const fight of fightsById.values()) {
		if (fight.eventId === eventId) return fight.id;
	}
	return null;
}

function parseBout(value: string): [string, string] {
	const parts = value.split(/\s+vs\.?\s+/i).map((part) => part.trim());
	if (parts.length !== 2 || !parts[0] || !parts[1]) {
		throw new Error(`Cannot parse bout: ${value}`);
	}
	return [parts[0], parts[1]];
}

function resolveFighterId(
	index: Map<string, string[]>,
	fightersById: Map<string, FighterImport>,
	name: string,
	context: string,
	weightClass?: string,
) {
	const matches = index.get(normalizeName(name)) ?? [];
	if (matches.length === 1) return matches[0];
	const targetWeight = weightClassLimit(weightClass);
	if (targetWeight !== null) {
		const weightMatches = matches.filter((id) => fightersById.get(id)?.weightLbs === targetWeight);
		if (weightMatches.length === 1) return weightMatches[0];
	}
	if (matches.length === 0) {
		const fuzzyMatches = fuzzyFighterMatches(fightersById, name, targetWeight);
		if (fuzzyMatches.length === 1) return fuzzyMatches[0];
	}
	if (matches.length > 1) {
		throw new Error(`Ambiguous fighter name ${name} in ${context}: ${matches.join(', ')}`);
	}
	throw new Error(`Unknown fighter name ${name} in ${context}`);
}

function resolveFightStatFighterId(
	resultImports: Map<string, ResultImport>,
	fightersById: Map<string, FighterImport>,
	fightId: string,
	name: string,
	context: string,
) {
	const normalized = normalizeName(name);
	const matches = [...resultImports.values()]
		.filter((result) => result.fightId === fightId)
		.filter((result) =>
			(fightersById.get(result.fighterId)?.aliases ?? []).some(
				(alias) => normalizeName(alias) === normalized,
			),
		)
		.map((result) => result.fighterId);
	if (matches.length === 1) return matches[0];
	if (matches.length === 0) {
		const fuzzyMatches = [...resultImports.values()]
			.filter((result) => result.fightId === fightId)
			.filter((result) =>
				(fightersById.get(result.fighterId)?.aliases ?? []).some(
					(alias) => editDistance(normalizeName(alias), normalized) <= 2,
				),
			)
			.map((result) => result.fighterId);
		if (fuzzyMatches.length === 1) return fuzzyMatches[0];
	}
	if (matches.length > 1) {
		throw new Error(`Ambiguous fighter name ${name} in ${context}: ${matches.join(', ')}`);
	}
	throw new Error(`Unknown fighter name ${name} in ${context}`);
}

function fuzzyFighterMatches(
	fightersById: Map<string, FighterImport>,
	name: string,
	targetWeight: number | null,
) {
	const normalized = normalizeName(name);
	return [...fightersById.values()]
		.filter((fighter) => targetWeight === null || fighter.weightLbs === targetWeight)
		.filter((fighter) =>
			fighter.aliases.some((alias) => editDistance(normalizeName(alias), normalized) <= 2),
		)
		.map((fighter) => fighter.id);
}

function parseOutcomes(
	value: string,
): ['win' | 'loss' | 'draw' | 'nc', 'win' | 'loss' | 'draw' | 'nc'] {
	const parts = value.split('/').map((part) => normalizeOutcome(part));
	if (parts.length !== 2) {
		throw new Error(`Cannot parse outcome pair: ${value}`);
	}
	return [parts[0], parts[1]];
}

function normalizeOutcome(value: string): 'win' | 'loss' | 'draw' | 'nc' {
	const normalized = value.trim().toLowerCase();
	if (normalized === 'w' || normalized === 'win') return 'win';
	if (normalized === 'l' || normalized === 'loss') return 'loss';
	if (normalized === 'd' || normalized === 'draw') return 'draw';
	return 'nc';
}

function parseStats(row: CsvRow) {
	return {
		knockdowns: parseInteger(row.KD),
		sigStrikesLanded: parseMadeAttempt(row['SIG.STR.']).made,
		sigStrikesAttempted: parseMadeAttempt(row['SIG.STR.']).attempt,
		totalStrikesLanded: parseMadeAttempt(row['TOTAL STR.']).made,
		totalStrikesAttempted: parseMadeAttempt(row['TOTAL STR.']).attempt,
		takedownsLanded: parseMadeAttempt(row.TD).made,
		takedownsAttempted: parseMadeAttempt(row.TD).attempt,
		subAttempts: parseInteger(row['SUB.ATT']),
		ctrlSeconds: parseClockSeconds(row.CTRL),
		reversals: parseInteger(row['REV.']),
	};
}

function addStats(result: ResultImport, stats: ReturnType<typeof parseStats>): ResultImport {
	return {
		...result,
		knockdowns: addNullable(result.knockdowns, stats.knockdowns),
		sigStrikesLanded: addNullable(result.sigStrikesLanded, stats.sigStrikesLanded),
		sigStrikesAttempted: addNullable(result.sigStrikesAttempted, stats.sigStrikesAttempted),
		totalStrikesLanded: addNullable(result.totalStrikesLanded, stats.totalStrikesLanded),
		totalStrikesAttempted: addNullable(result.totalStrikesAttempted, stats.totalStrikesAttempted),
		takedownsLanded: addNullable(result.takedownsLanded, stats.takedownsLanded),
		takedownsAttempted: addNullable(result.takedownsAttempted, stats.takedownsAttempted),
		subAttempts: addNullable(result.subAttempts, stats.subAttempts),
		ctrlSeconds: addNullable(result.ctrlSeconds, stats.ctrlSeconds),
		reversals: addNullable(result.reversals, stats.reversals),
	};
}

function addNullable(left: number | null, right: number | null) {
	if (left === null) return right;
	if (right === null) return left;
	return left + right;
}

function rememberFight(
	fighterFightIds: Map<string, Set<string>>,
	fighterLastFight: Map<string, { fightId: string; eventDate: string }>,
	fighterId: string,
	fightId: string,
	eventDate: string,
) {
	if (!fighterFightIds.has(fighterId)) {
		fighterFightIds.set(fighterId, new Set());
	}
	fighterFightIds.get(fighterId)?.add(fightId);

	const existing = fighterLastFight.get(fighterId);
	if (!existing || eventDate > existing.eventDate) {
		fighterLastFight.set(fighterId, { fightId, eventDate });
	}
}

function fightKey(eventName: string, bout: string) {
	return `${normalizeText(eventName)}|${normalizeText(bout)}`;
}

function resultKey(fightId: string, fighterId: string) {
	return `${fightId}|${fighterId}`;
}

function roundKey(fightId: string, fighterId: string, round: number) {
	return `${fightId}|${fighterId}|${round}`;
}

function normalizeText(value: string) {
	return value.trim().replace(/\s+/g, ' ').toLowerCase();
}

function normalizeName(value: string) {
	return normalizeText(value)
		.normalize('NFD')
		.replace(/[\u0300-\u036f]/g, '')
		.replace(/[.'’-]/g, '');
}

function editDistance(left: string, right: string) {
	const rows = left.length + 1;
	const columns = right.length + 1;
	const matrix = Array.from({ length: rows }, () => Array<number>(columns).fill(0));
	for (let row = 0; row < rows; row += 1) matrix[row][0] = row;
	for (let column = 0; column < columns; column += 1) matrix[0][column] = column;

	for (let row = 1; row < rows; row += 1) {
		for (let column = 1; column < columns; column += 1) {
			const cost = left[row - 1] === right[column - 1] ? 0 : 1;
			matrix[row][column] = Math.min(
				matrix[row - 1][column] + 1,
				matrix[row][column - 1] + 1,
				matrix[row - 1][column - 1] + cost,
			);
		}
	}

	return matrix[left.length][right.length];
}

function clean(value: string | undefined) {
	const trimmed = value?.trim();
	return trimmed && trimmed !== '--' ? trimmed : null;
}

function uniqueStrings(values: string[]) {
	return [...new Set(values.filter((value) => value.trim() !== ''))];
}

function extractUfcstatsId(url: string | undefined) {
	const match = url?.match(/\/([a-f0-9]{16})(?:[/?#].*)?$/i);
	return match?.[1] ?? null;
}

function parseDate(value: string | undefined) {
	if (!value || value === '--') return null;
	const parsed = new Date(value.replace(/\./g, ''));
	if (Number.isNaN(parsed.getTime())) return null;
	return parsed.toISOString().slice(0, 10);
}

function parseHeightInches(value: string | undefined) {
	if (!value || value === '--') return null;
	const match = value.match(/(\d+)'\s*(\d+)/);
	return match ? Number.parseInt(match[1], 10) * 12 + Number.parseInt(match[2], 10) : null;
}

function parseReachInches(value: string | undefined) {
	if (!value || value === '--') return null;
	const match = value.match(/\d+/);
	return match ? Number.parseInt(match[0], 10) : null;
}

function parseWeightPounds(value: string | undefined) {
	if (!value || value === '--') return null;
	const match = value.match(/\d+/);
	return match ? Number.parseInt(match[0], 10) : null;
}

function parseInteger(value: string | undefined) {
	if (!value) return null;
	const match = value.match(/\d+/);
	return match ? Number.parseInt(match[0], 10) : null;
}

function parseRound(value: string | undefined) {
	return parseInteger(value);
}

function parseClockSeconds(value: string | undefined) {
	if (!value) return null;
	const match = value.match(/(\d+):(\d+)/);
	if (!match) return null;
	return Number.parseInt(match[1], 10) * 60 + Number.parseInt(match[2], 10);
}

function parseFightElapsedSeconds(round: number | null, clock: string | undefined) {
	const clockSeconds = parseClockSeconds(clock);
	if (!round || clockSeconds === null) return clockSeconds;
	return (round - 1) * 5 * 60 + clockSeconds;
}

function parseScheduledRounds(value: string | undefined) {
	if (!value) return null;
	const match = value.match(/(\d+)\s*Rnd/i);
	return match ? Number.parseInt(match[1], 10) : null;
}

function parseMadeAttempt(value: string | undefined): {
	made: number | null;
	attempt: number | null;
} {
	if (!value) return { made: null, attempt: null };
	const match = value.match(/(\d+)\s+of\s+(\d+)/i);
	if (!match) return { made: parseInteger(value), attempt: null };
	return {
		made: Number.parseInt(match[1], 10),
		attempt: Number.parseInt(match[2], 10),
	};
}

function normalizeWeightClass(value: string | undefined) {
	const normalized = value
		?.replace(/\bUFC\b/gi, '')
		.replace(/\bTitle\b/gi, '')
		.replace(/\bBout\b/gi, '')
		.replace(/\s+/g, ' ')
		.trim()
		.toLowerCase();
	return normalized || null;
}

function weightClassLimit(value: string | undefined) {
	const normalized = value?.toLowerCase() ?? '';
	if (normalized.includes('strawweight')) return 115;
	if (normalized.includes('flyweight')) return 125;
	if (normalized.includes('bantamweight')) return 135;
	if (normalized.includes('featherweight')) return 145;
	if (normalized.includes('lightweight')) return 155;
	if (normalized.includes('welterweight')) return 170;
	if (normalized.includes('middleweight')) return 185;
	if (normalized.includes('light heavyweight')) return 205;
	if (normalized.includes('heavyweight')) return 265;
	return null;
}

if (import.meta.url === `file://${process.argv[1]}`) {
	main().catch(async (error) => {
		console.error(error instanceof Error ? error.message : error);
		await sql.end();
		process.exit(1);
	});
}
