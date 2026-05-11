'use client';

import { ExternalLink, Loader2, X } from 'lucide-react';
import type { Dispatch, SetStateAction } from 'react';
import { useCallback, useEffect, useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
	Sheet,
	SheetContent,
	SheetDescription,
	SheetHeader,
	SheetTitle,
} from '@/components/ui/sheet';
import { Skeleton } from '@/components/ui/skeleton';
import { DEBUG } from '@/lib/debug';
import {
	ageFromDob,
	cleanRecord,
	type FighterDetail,
	heightInches,
	parseNumeric,
	parsePct,
	reachInches,
	STAT_ROWS,
} from './upcoming-types';

type Target = {
	fightId: string;
	fighterA: { id: string; name: string };
	fighterB: { id: string; name: string };
	weightClass: string;
	eventName: string;
} | null;

type FighterState = {
	data: FighterDetail | null;
	loading: boolean;
	error: string | null;
};

type BackfillStatus = 'none' | 'current' | 'stale_count' | 'stale_stats' | 'in_progress' | 'failed';

type BackfillState = {
	fighter_id: string;
	status: BackfillStatus;
	last_backfilled_at: string | null;
	history_count_at_backfill: number;
	last_known_fight_id: string | null;
	last_error: string | null;
	new_fight_count?: number;
};

type BackfillJob = {
	job_id: string;
	fighter_id: string;
	status: 'in_progress' | 'completed' | 'failed';
	progress: { current: number; total: number; message: string };
	error: string | null;
	started_at: string;
	completed_at: string | null;
};

type FightPrediction = {
	fight_id: string;
	fighter_a_id: string;
	fighter_b_id: string;
	predicted_winner_id: string;
	win_prob: number;
	model_version: string;
	contributing_features: Array<{
		name: string;
		value: number | null;
		shap: number;
	}>;
	odds?: Array<{
		fighter_id: string;
		decimal_odds: number;
		american_odds: number;
		market_prob: number;
	}>;
	edge_pct?: number;
	market_prob?: number;
};

const INITIAL: FighterState = { data: null, loading: false, error: null };

export function CompareSheet({
	target,
	today,
	onClose,
}: {
	target: Target;
	today: Date;
	onClose: () => void;
}) {
	const [a, setA] = useState<FighterState>(INITIAL);
	const [b, setB] = useState<FighterState>(INITIAL);
	const [backfillStates, setBackfillStates] = useState<Record<string, BackfillState>>({});
	const [loadingIds, setLoadingIds] = useState<Set<string>>(() => new Set());
	const [jobProgress, setJobProgress] = useState<Record<string, string>>({});
	const [prediction, setPrediction] = useState<FightPrediction | null>(null);
	const [predictionLoading, setPredictionLoading] = useState(false);
	const [predictionError, setPredictionError] = useState<string | null>(null);
	const open = !!target;

	const fetchBackfillState = useCallback(async (fighterId: string) => {
		const res = await fetch(`/api/predict/backfill/state/${fighterId}`);
		if (!res.ok) throw new Error(`Backfill state ${fighterId} returned ${res.status}`);
		const state = (await res.json()) as BackfillState;
		setBackfillStates((prev) => ({ ...prev, [fighterId]: state }));
	}, []);

	const loadBackfill = useCallback(
		async (fighterId: string) => {
			setLoadingIds((prev) => new Set(prev).add(fighterId));
			try {
				const res = await fetch(`/api/predict/backfill/fighter/${fighterId}`, { method: 'POST' });
				if (!res.ok) throw new Error(`Backfill ${fighterId} returned ${res.status}`);
				const started = (await res.json()) as BackfillJob;
				setJobProgress((prev) => ({ ...prev, [fighterId]: started.progress.message }));
				await pollBackfillJob(started.job_id, fighterId, setJobProgress);
				await fetchBackfillState(fighterId);
			} catch (err) {
				setBackfillStates((prev) => ({
					...prev,
					[fighterId]: {
						fighter_id: fighterId,
						status: 'failed',
						last_backfilled_at: null,
						history_count_at_backfill: prev[fighterId]?.history_count_at_backfill ?? 0,
						last_known_fight_id: prev[fighterId]?.last_known_fight_id ?? null,
						last_error: err instanceof Error ? err.message : String(err),
						new_fight_count: 0,
					},
				}));
			} finally {
				setLoadingIds((prev) => {
					const next = new Set(prev);
					next.delete(fighterId);
					return next;
				});
				setJobProgress((prev) => {
					const next = { ...prev };
					delete next[fighterId];
					return next;
				});
			}
		},
		[fetchBackfillState],
	);

	useEffect(() => {
		if (!target) {
			setA(INITIAL);
			setB(INITIAL);
			setBackfillStates({});
			setLoadingIds(new Set());
			setJobProgress({});
			setPrediction(null);
			setPredictionLoading(false);
			setPredictionError(null);
			return;
		}
		let cancelled = false;
		const fetchOne = async (id: string, setter: (s: FighterState) => void) => {
			setter({ data: null, loading: true, error: null });
			DEBUG('compare-sheet', () => `fetch-fighter id=${id}`);
			try {
				const res = await fetch(`/api/ufcstats/fighter/${id}`);
				if (!res.ok) throw new Error(`Fighter ${id} returned ${res.status}`);
				const data = (await res.json()) as FighterDetail;
				if (cancelled) return;
				setter({ data, loading: false, error: null });
			} catch (err) {
				if (cancelled) return;
				const msg = err instanceof Error ? err.message : 'Failed to load fighter';
				DEBUG('compare-sheet', () => `fetch-fighter-failed id=${id} msg=${msg}`);
				setter({ data: null, loading: false, error: msg });
			}
		};
		// Fetch both in parallel — pure HTTP, no shared browser state.
		void fetchOne(target.fighterA.id, setA);
		void fetchOne(target.fighterB.id, setB);
		void fetchBackfillState(target.fighterA.id);
		void fetchBackfillState(target.fighterB.id);
		setPrediction(null);
		setPredictionError(null);
		setPredictionLoading(true);
		void fetch(`/api/predict/fight/${target.fightId}`)
			.then(async (res) => {
				const body = await res.json();
				if (!res.ok) {
					throw new Error(body.error ?? `Prediction ${target.fightId} returned ${res.status}`);
				}
				if (!cancelled) setPrediction(body as FightPrediction);
			})
			.catch((err) => {
				if (!cancelled) setPredictionError(err instanceof Error ? err.message : String(err));
			})
			.finally(() => {
				if (!cancelled) setPredictionLoading(false);
			});
		return () => {
			cancelled = true;
		};
	}, [fetchBackfillState, target]);

	const aBackfill = target ? backfillStates[target.fighterA.id] : undefined;
	const bBackfill = target ? backfillStates[target.fighterB.id] : undefined;
	const aLoading = target ? loadingIds.has(target.fighterA.id) : false;
	const bLoading = target ? loadingIds.has(target.fighterB.id) : false;

	return (
		<Sheet open={open} onOpenChange={(v) => !v && onClose()}>
			<SheetContent
				side="right"
				className="w-full sm:max-w-2xl overflow-y-auto p-0 flex flex-col gap-0"
			>
				<SheetHeader className="px-5 sm:px-6 py-4 border-b sticky top-0 bg-background z-10">
					<div className="flex items-start justify-between gap-3">
						<div className="min-w-0">
							<SheetTitle className="text-base sm:text-lg">Fighter Matchup</SheetTitle>
							<SheetDescription className="text-xs sm:text-sm">
								{target?.eventName} · {target?.weightClass}
							</SheetDescription>
						</div>
						<Button
							size="icon"
							variant="ghost"
							className="h-8 w-8 -mr-1.5"
							onClick={onClose}
							aria-label="Close comparison"
						>
							<X className="w-4 h-4" />
						</Button>
					</div>
				</SheetHeader>

				<div className="px-4 sm:px-6 py-5 flex flex-col gap-6">
					<FighterHeaderRow
						a={a}
						b={b}
						target={target}
						today={today}
						aBackfill={aBackfill}
						bBackfill={bBackfill}
						aLoading={aLoading}
						bLoading={bLoading}
						prediction={prediction}
						predictionLoading={predictionLoading}
					/>
					{target && (
						<BackfillActionPanel
							target={target}
							aState={aBackfill}
							bState={bBackfill}
							aLoading={aLoading}
							bLoading={bLoading}
							aProgress={jobProgress[target.fighterA.id]}
							bProgress={jobProgress[target.fighterB.id]}
							onLoadBackfill={loadBackfill}
						/>
					)}
					<ModelPickRow
						target={target}
						prediction={prediction}
						loading={predictionLoading}
						error={predictionError}
					/>
					<PhysicalsBlock a={a} b={b} today={today} />
					<StatsBlock a={a} b={b} />
					{(a.data || b.data) && (
						<div className="flex flex-wrap gap-2 justify-center text-xs">
							{a.data && (
								<Button asChild variant="outline" size="sm">
									<a href={a.data.url} target="_blank" rel="noreferrer noopener">
										<ExternalLink className="w-3.5 h-3.5 mr-1.5" />
										{a.data.name} on UFCStats
									</a>
								</Button>
							)}
							{b.data && (
								<Button asChild variant="outline" size="sm">
									<a href={b.data.url} target="_blank" rel="noreferrer noopener">
										<ExternalLink className="w-3.5 h-3.5 mr-1.5" />
										{b.data.name} on UFCStats
									</a>
								</Button>
							)}
						</div>
					)}
				</div>
			</SheetContent>
		</Sheet>
	);
}

function FighterHeaderRow({
	a,
	b,
	target,
	today,
	aBackfill,
	bBackfill,
	aLoading,
	bLoading,
	prediction,
	predictionLoading,
}: {
	a: FighterState;
	b: FighterState;
	target: Target;
	today: Date;
	aBackfill: BackfillState | undefined;
	bBackfill: BackfillState | undefined;
	aLoading: boolean;
	bLoading: boolean;
	prediction: FightPrediction | null;
	predictionLoading: boolean;
}) {
	return (
		<div className="grid grid-cols-[1fr_auto_1fr] gap-2 sm:gap-3 items-stretch">
			<HeaderCell
				state={a}
				fallbackName={target?.fighterA.name ?? 'Fighter A'}
				fighterId={target?.fighterA.id}
				accent="red"
				today={today}
				backfillState={aBackfill}
				backfillLoading={aLoading}
				prediction={prediction}
				predictionLoading={predictionLoading}
			/>
			<div className="flex items-center justify-center">
				<span className="text-xl sm:text-2xl font-extrabold text-muted-foreground tracking-widest">
					VS
				</span>
			</div>
			<HeaderCell
				state={b}
				fallbackName={target?.fighterB.name ?? 'Fighter B'}
				fighterId={target?.fighterB.id}
				accent="blue"
				today={today}
				align="right"
				backfillState={bBackfill}
				backfillLoading={bLoading}
				prediction={prediction}
				predictionLoading={predictionLoading}
			/>
		</div>
	);
}

function HeaderCell({
	state,
	fallbackName,
	fighterId,
	accent,
	align = 'left',
	today,
	backfillState,
	backfillLoading,
	prediction,
	predictionLoading,
}: {
	state: FighterState;
	fallbackName: string;
	fighterId: string | undefined;
	accent: 'red' | 'blue';
	align?: 'left' | 'right';
	today: Date;
	backfillState: BackfillState | undefined;
	backfillLoading: boolean;
	prediction: FightPrediction | null;
	predictionLoading: boolean;
}) {
	const accentClasses =
		accent === 'red' ? 'border-red-500/40 bg-red-500/5' : 'border-blue-500/40 bg-blue-500/5';
	const accentDot = accent === 'red' ? 'bg-red-500' : 'bg-blue-500';
	const f = state.data;
	const name = f?.name ?? fallbackName;
	const record = f ? cleanRecord(f.record) : null;
	const age = f?.info.dob ? ageFromDob(f.info.dob, today) : null;

	return (
		<div
			className={`rounded-lg border ${accentClasses} p-3 sm:p-4 flex flex-col gap-1 ${
				align === 'right' ? 'items-end text-right' : 'items-start text-left'
			}`}
		>
			<div className="flex items-center gap-1.5 text-[10px] sm:text-xs uppercase font-semibold tracking-wider text-muted-foreground">
				<span className={`w-1.5 h-1.5 rounded-full ${accentDot}`} aria-hidden />
				{accent === 'red' ? 'Corner A' : 'Corner B'}
			</div>
			<BackfillStatusBadge state={backfillState} loading={backfillLoading} />
			<ModelProbabilityBar
				fighterId={fighterId}
				prediction={prediction}
				loading={predictionLoading}
				align={align}
				accent={accent}
			/>
			{state.loading ? (
				<>
					<Skeleton className="h-5 w-32" />
					<Skeleton className="h-4 w-16 mt-1" />
				</>
			) : state.error ? (
				<>
					<span className="font-semibold text-sm sm:text-base leading-tight">{name}</span>
					<span className="text-xs text-destructive">Stats unavailable</span>
				</>
			) : (
				<>
					<span className="font-bold text-base sm:text-lg leading-tight">{name}</span>
					{f?.nickname && (
						<span className="text-xs text-muted-foreground italic truncate max-w-full">
							{f.nickname}
						</span>
					)}
					{record && (
						<Badge variant="secondary" className="font-mono text-xs mt-0.5">
							{record}
						</Badge>
					)}
					{age !== null && <span className="text-xs text-muted-foreground mt-0.5">{age} yrs</span>}
				</>
			)}
		</div>
	);
}

function BackfillActionPanel({
	target,
	aState,
	bState,
	aLoading,
	bLoading,
	aProgress,
	bProgress,
	onLoadBackfill,
}: {
	target: NonNullable<Target>;
	aState: BackfillState | undefined;
	bState: BackfillState | undefined;
	aLoading: boolean;
	bLoading: boolean;
	aProgress: string | undefined;
	bProgress: string | undefined;
	onLoadBackfill: (fighterId: string) => Promise<void>;
}) {
	const actions = [
		{
			fighter: target.fighterA,
			state: aState,
			loading: aLoading,
			progress: aProgress,
		},
		{
			fighter: target.fighterB,
			state: bState,
			loading: bLoading,
			progress: bProgress,
		},
	].filter((item) => canRunBackfill(item.state?.status, item.loading));

	if (!actions.length) return null;

	return (
		<div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
			{actions.map(({ fighter, state, loading, progress }) => (
				<Button
					key={fighter.id}
					type="button"
					variant="outline"
					size="sm"
					className="justify-center min-w-0"
					disabled={loading}
					onClick={() => void onLoadBackfill(fighter.id)}
				>
					{loading && <Loader2 className="w-3.5 h-3.5 mr-1.5 animate-spin" />}
					<span className="truncate">
						{fighter.name}: {loading ? (progress ?? 'Loading') : backfillActionLabel(state)}
					</span>
				</Button>
			))}
		</div>
	);
}

function BackfillStatusBadge({
	state,
	loading,
}: {
	state: BackfillState | undefined;
	loading: boolean;
}) {
	if (loading) {
		return (
			<Badge variant="outline" className="gap-1 text-[10px]">
				<Loader2 className="w-3 h-3 animate-spin" />
				Loading
			</Badge>
		);
	}
	const status = state?.status ?? 'none';
	const label =
		status === 'current'
			? 'Loaded'
			: status === 'stale_count'
				? `${state?.new_fight_count ?? 0} new`
				: status === 'stale_stats'
					? 'Stale'
					: status === 'failed'
						? 'Failed'
						: 'Not loaded';
	const className =
		status === 'current'
			? 'border-emerald-500/40 text-emerald-600'
			: status === 'stale_count' || status === 'stale_stats'
				? 'border-yellow-500/50 text-yellow-600'
				: status === 'failed'
					? 'border-destructive/50 text-destructive'
					: 'border-muted-foreground/30 text-muted-foreground';

	return (
		<Badge variant="outline" className={`text-[10px] ${className}`}>
			{label}
		</Badge>
	);
}

function ModelProbabilityBar({
	fighterId,
	prediction,
	loading,
	align,
	accent,
}: {
	fighterId: string | undefined;
	prediction: FightPrediction | null;
	loading: boolean;
	align: 'left' | 'right';
	accent: 'red' | 'blue';
}) {
	if (loading) {
		return (
			<div className="w-full max-w-36 flex flex-col gap-1 py-1">
				<Skeleton className="h-3 w-12" />
				<Skeleton className="h-2 w-full" />
			</div>
		);
	}
	const probability = fighterId && prediction ? probabilityForFighter(prediction, fighterId) : null;
	if (probability === null) return null;
	const fillClass = accent === 'red' ? 'bg-red-500' : 'bg-blue-500';
	return (
		<div
			className={`w-full max-w-36 flex flex-col gap-1 py-1 ${align === 'right' ? 'items-end' : 'items-start'}`}
		>
			<span className="text-xs font-mono font-semibold text-foreground">
				{Math.round(probability * 100)}%
			</span>
			<div className="h-2 w-full rounded-full bg-muted overflow-hidden">
				<div
					className={`h-full ${fillClass} transition-all duration-500`}
					style={{ width: `${Math.round(probability * 100)}%` }}
				/>
			</div>
		</div>
	);
}

function ModelPickRow({
	target,
	prediction,
	loading,
	error,
}: {
	target: Target;
	prediction: FightPrediction | null;
	loading: boolean;
	error: string | null;
}) {
	if (!target) return null;
	if (loading) {
		return (
			<div className="rounded-md border border-border/60 px-3 py-3">
				<Skeleton className="h-4 w-28 mx-auto" />
				<Skeleton className="h-3 w-44 mx-auto mt-2" />
			</div>
		);
	}
	if (!prediction) {
		return (
			<div className="rounded-md border border-border/60 px-3 py-2 text-center text-xs text-muted-foreground">
				{error ? 'Model pick unavailable' : 'Predictions ready when both fighters loaded'}
			</div>
		);
	}
	const winner =
		prediction.predicted_winner_id === target.fighterA.id ? target.fighterA : target.fighterB;
	const probability = probabilityForFighter(prediction, winner.id);
	const valueRows = valueRowsForPrediction(target, prediction);
	const valuePick = valueRows.every((row) => row.edge !== null)
		? valueRows.reduce((best, row) =>
				(row.edge ?? -Infinity) > (best.edge ?? -Infinity) ? row : best,
			)
		: null;
	const modelPickEdge = valueRows.find((row) => row.fighter.id === winner.id)?.edge ?? null;
	const valueDiffers = valuePick ? valuePick.fighter.id !== winner.id : false;

	return (
		<div className="rounded-md border border-border/70 bg-muted/20 px-3 py-3">
			<div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
				<SignalTile
					label="Model Pick"
					name={winner.name}
					primary={`${formatPct(probability)} win probability`}
					badge={
						modelPickEdge !== null
							? {
									text: `Edge ${formatSignedPct(modelPickEdge)}`,
									tone: edgeTone(modelPickEdge),
								}
							: null
					}
				/>
				<SignalTile
					label="Value Pick"
					name={valuePick?.fighter.name ?? 'Market odds unavailable'}
					primary={
						valuePick
							? `${formatSignedPct(valuePick.edge ?? 0)} vs market`
							: 'Need two matched moneylines'
					}
					badge={
						valuePick
							? {
									text: valueDiffers ? 'Differs from pick' : 'Same as pick',
									tone: valueDiffers ? 'amber' : 'green',
								}
							: null
					}
				/>
			</div>
			<div className="text-xs text-muted-foreground mt-2 text-center">
				Model {prediction.model_version}
			</div>
		</div>
	);
}

function SignalTile({
	label,
	name,
	primary,
	badge,
}: {
	label: string;
	name: string;
	primary: string;
	badge: { text: string; tone: 'green' | 'amber' | 'red' | 'neutral' } | null;
}) {
	return (
		<div className="rounded-md border border-border/60 bg-background/60 px-3 py-2 min-w-0 text-center">
			<div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
				{label}
			</div>
			<div className="text-sm font-semibold text-foreground mt-1 truncate">{name}</div>
			<div className="text-xs text-muted-foreground mt-0.5">{primary}</div>
			{badge && (
				<Badge variant="outline" className={`mt-2 text-xs ${edgeBadgeClass(badge.tone)}`}>
					{badge.text}
				</Badge>
			)}
		</div>
	);
}

function valueRowsForPrediction(target: NonNullable<Target>, prediction: FightPrediction) {
	const fighters = [target.fighterA, target.fighterB];
	return fighters.map((fighter) => {
		const market = prediction.odds?.find((row) => row.fighter_id === fighter.id);
		const modelProb = probabilityForFighter(prediction, fighter.id);
		return {
			fighter,
			edge: market ? modelProb - market.market_prob : null,
		};
	});
}

function probabilityForFighter(prediction: FightPrediction, fighterId: string): number {
	return prediction.predicted_winner_id === fighterId
		? prediction.win_prob
		: 1 - prediction.win_prob;
}

function formatSignedPct(value: number): string {
	const pct = Math.round(value * 100);
	return `${pct > 0 ? '+' : ''}${pct}%`;
}

function formatPct(value: number): string {
	return `${Math.round(value * 100)}%`;
}

function edgeTone(value: number): 'green' | 'amber' | 'red' | 'neutral' {
	if (value >= 0.1) return 'green';
	if (value >= 0.05) return 'amber';
	if (value < 0) return 'red';
	return 'neutral';
}

function edgeBadgeClass(tone: 'green' | 'amber' | 'red' | 'neutral'): string {
	if (tone === 'green') return 'border-emerald-500/50 text-emerald-600 bg-emerald-500/10';
	if (tone === 'amber') return 'border-yellow-500/50 text-yellow-700 bg-yellow-500/10';
	if (tone === 'red') return 'border-destructive/50 text-destructive bg-destructive/10';
	return 'border-muted-foreground/30 text-muted-foreground';
}

function PhysicalsBlock({ a, b, today }: { a: FighterState; b: FighterState; today: Date }) {
	const rows: Array<{
		label: string;
		extract: (f: FighterDetail) => string | null;
		numeric?: (f: FighterDetail) => number | null;
		higherWins?: boolean;
	}> = [
		{
			label: 'Height',
			extract: (f) => f.info.height || null,
			numeric: (f) => heightInches(f.info.height),
			higherWins: true,
		},
		{
			label: 'Reach',
			extract: (f) => f.info.reach || null,
			numeric: (f) => reachInches(f.info.reach),
			higherWins: true,
		},
		{
			label: 'Weight',
			extract: (f) => f.info.weight || null,
		},
		{
			label: 'Stance',
			extract: (f) => f.info.stance || null,
		},
		{
			label: 'Age',
			extract: (f) => {
				const age = ageFromDob(f.info.dob, today);
				return age !== null ? `${age}` : null;
			},
			numeric: (f) => ageFromDob(f.info.dob, today),
			higherWins: false,
		},
	];

	return (
		<section>
			<h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground pb-2">
				Physicals
			</h3>
			<div className="rounded-lg border border-border/60 overflow-hidden">
				{rows.map((row, idx) => {
					const aVal = a.data ? row.extract(a.data) : null;
					const bVal = b.data ? row.extract(b.data) : null;
					const aN = a.data && row.numeric ? row.numeric(a.data) : null;
					const bN = b.data && row.numeric ? row.numeric(b.data) : null;
					const aWins = aN !== null && bN !== null ? (row.higherWins ? aN > bN : aN < bN) : false;
					const bWins = aN !== null && bN !== null ? (row.higherWins ? bN > aN : bN < aN) : false;
					return (
						<div
							key={row.label}
							className={`grid grid-cols-[1fr_auto_1fr] items-center gap-2 px-3 py-2 ${
								idx > 0 ? 'border-t border-border/60' : ''
							}`}
						>
							<span
								className={`text-sm font-medium text-left ${aWins ? 'text-foreground' : 'text-muted-foreground'}`}
							>
								{a.loading ? <Skeleton className="h-4 w-16" /> : (aVal ?? '—')}
							</span>
							<span className="text-[10px] sm:text-xs text-muted-foreground/70 uppercase tracking-wider px-2">
								{row.label}
							</span>
							<span
								className={`text-sm font-medium text-right ${bWins ? 'text-foreground' : 'text-muted-foreground'}`}
							>
								{b.loading ? <Skeleton className="h-4 w-16 ml-auto" /> : (bVal ?? '—')}
							</span>
						</div>
					);
				})}
			</div>
		</section>
	);
}

function StatsBlock({ a, b }: { a: FighterState; b: FighterState }) {
	if (a.error && b.error) {
		return (
			<Alert variant="destructive">
				<AlertDescription>
					Couldn't load stats for either fighter. Try closing and reopening this comparison.
				</AlertDescription>
			</Alert>
		);
	}

	return (
		<section>
			<h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground pb-2">
				Career Stats
			</h3>
			{(a.error || b.error) && (
				<Alert variant="destructive" className="mb-3">
					<AlertDescription className="text-xs">
						Stats unavailable for{' '}
						{[a.error && a.data?.name, b.error && b.data?.name].filter(Boolean).join(' & ') ||
							'one fighter'}
						. Showing partial comparison.
					</AlertDescription>
				</Alert>
			)}
			<div className="rounded-lg border border-border/60 overflow-hidden">
				{STAT_ROWS.map((row, idx) => (
					<StatRow
						key={row.key}
						label={row.label}
						aRaw={a.data?.info[row.key]}
						bRaw={b.data?.info[row.key]}
						kind={row.kind}
						higherWins={row.higherWins}
						loading={a.loading || b.loading}
						topBorder={idx > 0}
					/>
				))}
			</div>
		</section>
	);
}

function StatRow({
	label,
	aRaw,
	bRaw,
	kind,
	higherWins,
	loading,
	topBorder,
}: {
	label: string;
	aRaw: string | undefined;
	bRaw: string | undefined;
	kind: 'numeric' | 'percent';
	higherWins: boolean;
	loading: boolean;
	topBorder: boolean;
}) {
	const aN = kind === 'percent' ? parsePct(aRaw) : parseNumeric(aRaw);
	const bN = kind === 'percent' ? parsePct(bRaw) : parseNumeric(bRaw);
	const aDisplay = aRaw ?? '—';
	const bDisplay = bRaw ?? '—';

	let aWidth = 0;
	let bWidth = 0;
	if (aN !== null && bN !== null) {
		const max = Math.max(aN, bN, 0.0001);
		aWidth = (aN / max) * 100;
		bWidth = (bN / max) * 100;
	} else if (aN !== null) {
		aWidth = 100;
	} else if (bN !== null) {
		bWidth = 100;
	}
	const aWins = aN !== null && bN !== null ? (higherWins ? aN > bN : aN < bN) : false;
	const bWins = aN !== null && bN !== null ? (higherWins ? bN > aN : bN < aN) : false;

	return (
		<div className={`px-3 py-3 ${topBorder ? 'border-t border-border/60' : ''}`}>
			<div className="flex items-center justify-center text-[10px] sm:text-xs text-muted-foreground/70 uppercase tracking-wider pb-2">
				{label}
			</div>
			<div className="grid grid-cols-2 gap-3 sm:gap-4">
				<BarCell value={aDisplay} widthPct={aWidth} winning={aWins} side="left" loading={loading} />
				<BarCell
					value={bDisplay}
					widthPct={bWidth}
					winning={bWins}
					side="right"
					loading={loading}
				/>
			</div>
		</div>
	);
}

function BarCell({
	value,
	widthPct,
	winning,
	side,
	loading,
}: {
	value: string;
	widthPct: number;
	winning: boolean;
	side: 'left' | 'right';
	loading: boolean;
}) {
	if (loading) {
		return <Skeleton className="h-7 w-full" />;
	}
	const accent = side === 'left' ? 'red' : 'blue';
	const fillClass = winning
		? accent === 'red'
			? 'bg-red-500/80'
			: 'bg-blue-500/80'
		: 'bg-muted-foreground/20';
	const textClass = winning ? 'text-foreground font-bold' : 'text-muted-foreground';

	return (
		<div className={`flex flex-col gap-1 ${side === 'left' ? 'items-end' : 'items-start'}`}>
			<span className={`text-sm font-mono ${textClass}`}>{value}</span>
			<div
				className={`relative w-full h-2 bg-muted/40 rounded-full overflow-hidden ${
					side === 'left' ? 'flex justify-end' : ''
				}`}
			>
				<div
					className={`h-full ${fillClass} transition-all duration-500`}
					style={{ width: `${Math.max(0, Math.min(100, widthPct))}%` }}
				/>
			</div>
		</div>
	);
}

function canRunBackfill(status: BackfillStatus | undefined, loading: boolean): boolean {
	return (
		status === 'none' ||
		status === 'failed' ||
		status === 'stale_count' ||
		status === 'stale_stats' ||
		(status === 'in_progress' && !loading)
	);
}

function backfillActionLabel(state: BackfillState | undefined): string {
	if (state?.status === 'stale_count') {
		const count = state.new_fight_count ?? 0;
		return `Update — ${count} new ${count === 1 ? 'fight' : 'fights'}`;
	}
	if (state?.status === 'stale_stats') return 'Update';
	if (state?.status === 'failed') return 'Retry';
	return 'Load';
}

async function pollBackfillJob(
	jobId: string,
	fighterId: string,
	setJobProgress: Dispatch<SetStateAction<Record<string, string>>>,
): Promise<void> {
	while (true) {
		await sleep(1000);
		const res = await fetch(`/api/predict/backfill/job/${jobId}`);
		if (res.status === 404) {
			throw new Error('Backfill job disappeared. Click Load to retry.');
		}
		if (!res.ok) throw new Error(`Backfill job ${jobId} returned ${res.status}`);
		const job = (await res.json()) as BackfillJob;
		setJobProgress((prev) => ({ ...prev, [fighterId]: job.progress.message }));
		if (job.status === 'completed') return;
		if (job.status === 'failed') throw new Error(job.error ?? 'Backfill failed');
	}
}

function sleep(ms: number): Promise<void> {
	return new Promise((resolve) => setTimeout(resolve, ms));
}
