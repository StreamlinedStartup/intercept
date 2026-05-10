/**
 * Types + helpers for the Upcoming Fights dashboard.
 *
 * Mirrors the JSON shape returned by the @interceptor/domain-ufcstats routes:
 *   GET /api/ufcstats/events/upcoming
 *   GET /api/ufcstats/event/:id
 *   GET /api/ufcstats/fighter/:id
 */

export type UpcomingEvent = {
	id: string;
	name: string;
	date: string; // "May 09, 2026"
	location: string;
	url: string;
};

export type UpcomingResponse = {
	count: number;
	events: UpcomingEvent[];
};

export type FightCardEntry = {
	fightId: string | null;
	fightUrl: string | null;
	result: string | null;
	fighters: Array<{ name: string; id: string | null }>;
	stats: {
		knockdowns: [string, string];
		strikes: [string, string];
		takedowns: [string, string];
		submissions: [string, string];
	};
	weightClass: string;
	method: string;
	methodDetail: string | null;
	round: string;
	time: string;
};

export type EventDetail = {
	id: string;
	name: string;
	info: { date?: string; location?: string; attendance?: string } & Record<string, string>;
	fights: FightCardEntry[];
	fightCount: number;
	url: string;
};

export type FighterInfo = {
	height: string;
	weight: string;
	reach: string;
	stance: string;
	dob: string;
	slpm: string;
	str_acc: string;
	sapm: string;
	str_def: string;
	td_avg: string;
	td_acc: string;
	td_def: string;
	sub_avg: string;
} & Record<string, string>;

export type FighterDetail = {
	id: string;
	name: string;
	nickname: string | null;
	record: string; // "Record: 15-0-0"
	info: FighterInfo;
	historyCount: number;
	url: string;
};

/**
 * Parse "May 09, 2026" → Date. Returns null if unparseable.
 */
export function parseUfcDate(s: string | undefined | null): Date | null {
	if (!s) return null;
	const t = Date.parse(s);
	return Number.isFinite(t) ? new Date(t) : null;
}

/**
 * Today + N-day window check. Both bounds inclusive.
 * Anchored to the project's "today" rule — uses the runtime clock; if the
 * runtime clock is stable (set by the env), substitute that.
 */
export function isInWindow(eventDate: Date, today: Date, days: number): boolean {
	const start = new Date(today.getFullYear(), today.getMonth(), today.getDate());
	const end = new Date(start);
	end.setDate(end.getDate() + days);
	return eventDate >= start && eventDate <= end;
}

/**
 * Friendly relative date: "Today", "Tomorrow", "Sat May 16".
 */
export function friendlyDate(d: Date, today: Date): string {
	const start = new Date(today.getFullYear(), today.getMonth(), today.getDate());
	const e = new Date(d.getFullYear(), d.getMonth(), d.getDate());
	const dayDiff = Math.round((e.getTime() - start.getTime()) / 86_400_000);
	if (dayDiff === 0) return 'Today';
	if (dayDiff === 1) return 'Tomorrow';
	return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
}

/**
 * Strip "Record: " prefix.
 */
export function cleanRecord(record: string | undefined): string {
	return (record ?? '').replace(/^Record:\s*/i, '');
}

/**
 * Compute age from "May 01, 1994" relative to today. Returns null if unparseable.
 */
export function ageFromDob(dob: string | undefined, today: Date): number | null {
	const d = parseUfcDate(dob);
	if (!d) return null;
	let age = today.getFullYear() - d.getFullYear();
	const m = today.getMonth() - d.getMonth();
	if (m < 0 || (m === 0 && today.getDate() < d.getDate())) age -= 1;
	return age;
}

/**
 * Convert a height like `6' 2"` to total inches. Returns null if unparseable.
 */
export function heightInches(s: string | undefined): number | null {
	if (!s) return null;
	const m = s.match(/(\d+)'\s*(\d+)/);
	if (!m) return null;
	return Number(m[1]) * 12 + Number(m[2]);
}

/**
 * Strip the trailing inch mark from a reach string ("75\"" → 75).
 */
export function reachInches(s: string | undefined): number | null {
	if (!s) return null;
	const m = s.match(/(\d+)/);
	return m ? Number(m[1]) : null;
}

/**
 * Parse a percent string ("60%" → 0.6). Returns null on "--" or unparseable.
 */
export function parsePct(s: string | undefined): number | null {
	if (!s || s.includes('--')) return null;
	const m = s.match(/(\d+)/);
	return m ? Number(m[1]) / 100 : null;
}

/**
 * Parse a numeric stat ("4.04", "1.8") to a float. Null on "--".
 */
export function parseNumeric(s: string | undefined): number | null {
	if (!s || s.includes('--')) return null;
	const v = Number.parseFloat(s);
	return Number.isFinite(v) ? v : null;
}

/**
 * Stat row definitions for the comparison view. `higherWins` indicates
 * which direction is "better" — used to color the visual bar.
 */
export const STAT_ROWS: Array<{
	key: keyof FighterInfo;
	label: string;
	tooltip: string;
	kind: 'numeric' | 'percent';
	higherWins: boolean;
}> = [
	{
		key: 'slpm',
		label: 'Strikes Landed / min',
		tooltip: 'Significant strikes landed per minute',
		kind: 'numeric',
		higherWins: true,
	},
	{
		key: 'str_acc',
		label: 'Striking Accuracy',
		tooltip: 'Significant strike accuracy %',
		kind: 'percent',
		higherWins: true,
	},
	{
		key: 'sapm',
		label: 'Strikes Absorbed / min',
		tooltip: 'Significant strikes absorbed per minute (lower is better)',
		kind: 'numeric',
		higherWins: false,
	},
	{
		key: 'str_def',
		label: 'Striking Defense',
		tooltip: 'Significant strike defense %',
		kind: 'percent',
		higherWins: true,
	},
	{
		key: 'td_avg',
		label: 'Takedowns / 15min',
		tooltip: 'Takedown average per 15 minutes',
		kind: 'numeric',
		higherWins: true,
	},
	{
		key: 'td_acc',
		label: 'Takedown Accuracy',
		tooltip: 'Takedown accuracy %',
		kind: 'percent',
		higherWins: true,
	},
	{
		key: 'td_def',
		label: 'Takedown Defense',
		tooltip: 'Takedown defense %',
		kind: 'percent',
		higherWins: true,
	},
	{
		key: 'sub_avg',
		label: 'Submission Avg',
		tooltip: 'Submission attempts per 15 minutes',
		kind: 'numeric',
		higherWins: true,
	},
];
