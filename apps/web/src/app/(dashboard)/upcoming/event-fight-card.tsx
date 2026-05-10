'use client';

import { Check, ChevronRight, Loader2, Star } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import type { EventDetail, FightCardEntry } from './upcoming-types';

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
	predicted_winner_id: string;
	win_prob: number;
	model_version: string;
	contributing_features: Array<{
		name: string;
		value: number | null;
		shap: number;
	}>;
};

type EventPredictionResponse = {
	event_id: string;
	predictions: FightPrediction[];
	skipped: Array<{
		fight_id: string;
		reason: string;
		fighters?: Array<{ fighter_id: string; backfill_status: string }>;
	}>;
};

/**
 * Renders the list of fights on an event card. The first row is the
 * headlining matchup and gets visual emphasis; the rest collapse into a
 * dense list. Every row exposes a "Compare" button that opens the
 * side-by-side stat sheet.
 */
export function EventFightCard({
	detail,
	onCompare,
}: {
	detail: EventDetail;
	onCompare: (
		a: { id: string; name: string },
		b: { id: string; name: string },
		weightClass: string,
	) => void;
}) {
	const fighterIds = useMemo(() => {
		const ids = new Set<string>();
		for (const fight of detail.fights) {
			for (const fighter of fight.fighters) {
				if (fighter.id) ids.add(fighter.id);
			}
		}
		return [...ids];
	}, [detail.fights]);
	const [backfillStates, setBackfillStates] = useState<Record<string, BackfillState>>({});
	const [loadingIds, setLoadingIds] = useState<Set<string>>(() => new Set());
	const [jobProgress, setJobProgress] = useState<Record<string, string>>({});
	const [predictions, setPredictions] = useState<Record<string, FightPrediction>>({});
	const [predictionsLoading, setPredictionsLoading] = useState(false);
	const [predictionErrors, setPredictionErrors] = useState<Record<string, string>>({});

	const fetchBackfillState = useCallback(async (fighterId: string) => {
		const res = await fetch(`/api/predict/backfill/state/${fighterId}`);
		if (!res.ok) throw new Error(`Backfill state ${fighterId} returned ${res.status}`);
		const state = (await res.json()) as BackfillState;
		setBackfillStates((prev) => ({ ...prev, [fighterId]: state }));
	}, []);

	useEffect(() => {
		for (const fighterId of fighterIds) {
			void fetchBackfillState(fighterId);
		}
	}, [fetchBackfillState, fighterIds]);

	useEffect(() => {
		const readyFightIds = detail.fights
			.map((fight, index) => {
				const [a, b] = fight.fighters;
				if (!a?.id || !b?.id) return null;
				if (
					backfillStates[a.id]?.status !== 'current' ||
					backfillStates[b.id]?.status !== 'current'
				) {
					return null;
				}
				return resolveFightId(detail.id, index, fight);
			})
			.filter((fightId): fightId is string => Boolean(fightId));

		if (readyFightIds.length === 0 || predictionsLoading) return;
		if (readyFightIds.every((fightId) => predictions[fightId] || predictionErrors[fightId])) {
			return;
		}

		setPredictionsLoading(true);
		void fetch(`/api/predict/event/${detail.id}`)
			.then(async (res) => {
				const body = await res.json();
				if (!res.ok) {
					throw new Error(body.error ?? `Event predictions ${detail.id} returned ${res.status}`);
				}
				const result = body as EventPredictionResponse;
				setPredictions((prev) => ({
					...prev,
					...Object.fromEntries(
						result.predictions.map((prediction) => [prediction.fight_id, prediction]),
					),
				}));
				setPredictionErrors((prev) => {
					const next = { ...prev };
					for (const prediction of result.predictions) {
						delete next[prediction.fight_id];
					}
					for (const skipped of result.skipped) {
						next[skipped.fight_id] = skipped.reason;
					}
					return next;
				});
			})
			.catch((err) => {
				const message = err instanceof Error ? err.message : String(err);
				setPredictionErrors((prev) => ({
					...prev,
					...Object.fromEntries(readyFightIds.map((fightId) => [fightId, message])),
				}));
			})
			.finally(() => setPredictionsLoading(false));
	}, [backfillStates, detail.fights, detail.id, predictionErrors, predictions, predictionsLoading]);

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

	if (!detail.fights.length) {
		return (
			<div className="text-sm text-muted-foreground py-4 text-center">
				Fight card not yet announced.
			</div>
		);
	}

	const [headliner, ...rest] = detail.fights;

	return (
		<div className="flex flex-col gap-4">
			<HeadlinerRow
				eventId={detail.id}
				fightIndex={0}
				fight={headliner}
				backfillStates={backfillStates}
				loadingIds={loadingIds}
				jobProgress={jobProgress}
				predictions={predictions}
				predictionsLoading={predictionsLoading}
				predictionErrors={predictionErrors}
				onCompare={onCompare}
				onLoadBackfill={loadBackfill}
			/>
			{rest.length > 0 && (
				<div className="flex flex-col">
					<div className="text-xs font-semibold text-muted-foreground uppercase tracking-wide pb-2">
						Full Card · {rest.length} more {rest.length === 1 ? 'fight' : 'fights'}
					</div>
					<div className="flex flex-col rounded-md border border-border/60 divide-y divide-border/60">
						{rest.map((fight, idx) => (
							<FightRow
								key={
									fight.fightId ?? `${fight.fighters.map((f) => f.id ?? f.name).join('-')}-${idx}`
								}
								eventId={detail.id}
								fightIndex={idx + 1}
								fight={fight}
								backfillStates={backfillStates}
								loadingIds={loadingIds}
								jobProgress={jobProgress}
								predictions={predictions}
								predictionsLoading={predictionsLoading}
								predictionErrors={predictionErrors}
								onCompare={onCompare}
								onLoadBackfill={loadBackfill}
							/>
						))}
					</div>
				</div>
			)}
		</div>
	);
}

function HeadlinerRow({
	eventId,
	fightIndex,
	fight,
	backfillStates,
	loadingIds,
	jobProgress,
	predictions,
	predictionsLoading,
	predictionErrors,
	onCompare,
	onLoadBackfill,
}: {
	eventId: string;
	fightIndex: number;
	fight: FightCardEntry;
	backfillStates: Record<string, BackfillState>;
	loadingIds: Set<string>;
	jobProgress: Record<string, string>;
	predictions: Record<string, FightPrediction>;
	predictionsLoading: boolean;
	predictionErrors: Record<string, string>;
	onCompare: (
		a: { id: string; name: string },
		b: { id: string; name: string },
		weightClass: string,
	) => void;
	onLoadBackfill: (fighterId: string) => Promise<void>;
}) {
	const [a, b] = fight.fighters;
	const compareDisabled = !a?.id || !b?.id;
	const fightId = resolveFightId(eventId, fightIndex, fight);
	return (
		<div className="rounded-lg border border-red-500/30 bg-gradient-to-br from-red-500/5 to-transparent p-4 sm:p-5">
			<div className="flex items-center gap-2 mb-3 flex-wrap">
				<Star className="w-4 h-4 text-red-500 fill-red-500" />
				<span className="text-xs font-semibold uppercase tracking-wide text-red-500">
					Main Event
				</span>
				<Badge variant="outline" className="ml-auto text-xs">
					{fight.weightClass}
				</Badge>
				<PredictionChip
					className="ml-0"
					fight={fight}
					prediction={predictions[fightId]}
					loading={predictionsLoading && !predictions[fightId] && !predictionErrors[fightId]}
					error={predictionErrors[fightId]}
					backfillStates={backfillStates}
				/>
			</div>
			<div className="grid grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] gap-3 sm:gap-4 items-center">
				<FighterCell
					side="left"
					fighter={a}
					state={a?.id ? backfillStates[a.id] : undefined}
					loading={a?.id ? loadingIds.has(a.id) : false}
					progressText={a?.id ? jobProgress[a.id] : undefined}
					onLoadBackfill={onLoadBackfill}
				/>
				<div className="flex flex-col items-center gap-1">
					<span className="text-2xl sm:text-3xl font-bold tracking-widest text-muted-foreground">
						VS
					</span>
				</div>
				<FighterCell
					side="right"
					fighter={b}
					state={b?.id ? backfillStates[b.id] : undefined}
					loading={b?.id ? loadingIds.has(b.id) : false}
					progressText={b?.id ? jobProgress[b.id] : undefined}
					onLoadBackfill={onLoadBackfill}
				/>
			</div>
			<div className="mt-4 flex justify-center">
				<Button
					size="sm"
					disabled={compareDisabled}
					onClick={() => {
						if (a?.id && b?.id) {
							onCompare({ id: a.id, name: a.name }, { id: b.id, name: b.name }, fight.weightClass);
						}
					}}
				>
					{compareDisabled ? 'Stats unavailable' : 'Compare Fighters'}
					{!compareDisabled && <ChevronRight className="w-4 h-4 ml-1" />}
				</Button>
			</div>
		</div>
	);
}

function FighterCell({
	side,
	fighter,
	state,
	loading,
	progressText,
	onLoadBackfill,
}: {
	side: 'left' | 'right';
	fighter: { id: string | null; name: string } | undefined;
	state: BackfillState | undefined;
	loading: boolean;
	progressText: string | undefined;
	onLoadBackfill: (fighterId: string) => Promise<void>;
}) {
	const status = state?.status;
	const fighterId = fighter?.id;
	const canLoad = Boolean(fighterId) && canRunBackfill(status, loading);
	const buttonLabel = loading ? (progressText ?? 'Loading') : backfillActionLabel(state);
	return (
		<div
			className={`flex flex-col gap-1.5 min-w-0 ${side === 'left' ? 'items-start text-left' : 'items-end text-right'}`}
		>
			<span className="text-base sm:text-lg font-semibold leading-tight break-words">
				{fighter?.name ?? 'TBA'}
			</span>
			{fighter?.id && (
				<div className={`flex items-center gap-1.5 ${side === 'right' ? 'flex-row-reverse' : ''}`}>
					<BackfillDot status={status} loading={loading} />
					{(canLoad || loading) && (
						<Button
							type="button"
							size="sm"
							variant="outline"
							className="h-6 px-2 text-xs max-w-full"
							disabled={loading}
							onClick={(event) => {
								event.stopPropagation();
								if (fighterId) void onLoadBackfill(fighterId);
							}}
						>
							{loading && <Loader2 className="w-3 h-3 mr-1 animate-spin" />}
							<span className="truncate">{buttonLabel}</span>
						</Button>
					)}
				</div>
			)}
		</div>
	);
}

function FightRow({
	eventId,
	fightIndex,
	fight,
	backfillStates,
	loadingIds,
	jobProgress,
	predictions,
	predictionsLoading,
	predictionErrors,
	onCompare,
	onLoadBackfill,
}: {
	eventId: string;
	fightIndex: number;
	fight: FightCardEntry;
	backfillStates: Record<string, BackfillState>;
	loadingIds: Set<string>;
	jobProgress: Record<string, string>;
	predictions: Record<string, FightPrediction>;
	predictionsLoading: boolean;
	predictionErrors: Record<string, string>;
	onCompare: (
		a: { id: string; name: string },
		b: { id: string; name: string },
		weightClass: string,
	) => void;
	onLoadBackfill: (fighterId: string) => Promise<void>;
}) {
	const [a, b] = fight.fighters;
	const canCompare = !!a?.id && !!b?.id;
	const fightId = resolveFightId(eventId, fightIndex, fight);
	return (
		<div className="flex items-center gap-3 px-3 sm:px-4 py-3 text-left hover:bg-muted/50 transition-colors min-h-[52px]">
			<div className="flex-1 min-w-0 grid grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-center gap-2">
				<CompactFighterCell
					side="left"
					fighter={a}
					state={a?.id ? backfillStates[a.id] : undefined}
					loading={a?.id ? loadingIds.has(a.id) : false}
					progressText={a?.id ? jobProgress[a.id] : undefined}
					onLoadBackfill={onLoadBackfill}
				/>
				<span className="text-xs text-muted-foreground tracking-widest font-medium">VS</span>
				<CompactFighterCell
					side="right"
					fighter={b}
					state={b?.id ? backfillStates[b.id] : undefined}
					loading={b?.id ? loadingIds.has(b.id) : false}
					progressText={b?.id ? jobProgress[b.id] : undefined}
					onLoadBackfill={onLoadBackfill}
				/>
			</div>
			<Badge variant="outline" className="text-xs flex-shrink-0 hidden sm:inline-flex">
				{fight.weightClass}
			</Badge>
			<PredictionChip
				fight={fight}
				prediction={predictions[fightId]}
				loading={predictionsLoading && !predictions[fightId] && !predictionErrors[fightId]}
				error={predictionErrors[fightId]}
				backfillStates={backfillStates}
			/>
			<Button
				type="button"
				size="icon"
				variant="ghost"
				className="size-8 flex-shrink-0"
				disabled={!canCompare}
				aria-label={canCompare ? `Compare ${a?.name} vs ${b?.name}` : `${a?.name} vs ${b?.name}`}
				onClick={() => {
					if (canCompare && a?.id && b?.id) {
						onCompare({ id: a.id, name: a.name }, { id: b.id, name: b.name }, fight.weightClass);
					}
				}}
			>
				<ChevronRight className="w-4 h-4 text-muted-foreground" aria-hidden />
			</Button>
		</div>
	);
}

function PredictionChip({
	fight,
	prediction,
	loading,
	error,
	backfillStates,
	className = '',
}: {
	fight: FightCardEntry;
	prediction: FightPrediction | undefined;
	loading: boolean;
	error: string | undefined;
	backfillStates: Record<string, BackfillState>;
	className?: string;
}) {
	const [a, b] = fight.fighters;
	const ready = Boolean(
		a?.id &&
			b?.id &&
			backfillStates[a.id]?.status === 'current' &&
			backfillStates[b.id]?.status === 'current',
	);

	if (!ready) {
		return (
			<Badge
				variant="secondary"
				className={`text-xs text-muted-foreground bg-muted/60 whitespace-nowrap ${className}`}
			>
				Backfill required
			</Badge>
		);
	}

	if (loading) {
		return (
			<Badge variant="secondary" className={`text-xs gap-1 whitespace-nowrap ${className}`}>
				<Loader2 className="w-3 h-3 animate-spin" />
				Predicting
			</Badge>
		);
	}

	if (!prediction || error) {
		return (
			<Badge
				variant="secondary"
				className={`text-xs text-muted-foreground whitespace-nowrap ${className}`}
			>
				Unavailable
			</Badge>
		);
	}

	const winner = fight.fighters.find((fighter) => fighter.id === prediction.predicted_winner_id);
	return (
		<Badge
			className={`text-xs gap-1 bg-emerald-600 hover:bg-emerald-600 text-white whitespace-nowrap ${className}`}
		>
			<span className="truncate max-w-32">
				{Math.round(prediction.win_prob * 100)}% {winner?.name ?? 'Pick'}
			</span>
			<Check className="w-3 h-3" />
		</Badge>
	);
}

function CompactFighterCell({
	side,
	fighter,
	state,
	loading,
	progressText,
	onLoadBackfill,
}: {
	side: 'left' | 'right';
	fighter: { id: string | null; name: string } | undefined;
	state: BackfillState | undefined;
	loading: boolean;
	progressText: string | undefined;
	onLoadBackfill: (fighterId: string) => Promise<void>;
}) {
	const status = state?.status;
	const fighterId = fighter?.id;
	const canLoad = Boolean(fighterId) && canRunBackfill(status, loading);
	const buttonLabel = loading ? (progressText ?? 'Loading') : backfillActionLabel(state);
	return (
		<div
			className={`min-w-0 flex flex-col gap-1 ${side === 'right' ? 'items-end text-right' : 'items-start text-left'}`}
		>
			<span className="font-medium text-sm sm:text-base truncate max-w-full">
				{fighter?.name ?? 'TBA'}
			</span>
			{fighter?.id && (
				<div className={`flex items-center gap-1.5 ${side === 'right' ? 'flex-row-reverse' : ''}`}>
					<BackfillDot status={status} loading={loading} />
					{(canLoad || loading) && (
						<Button
							type="button"
							size="sm"
							variant="outline"
							className="h-6 px-2 text-xs max-w-full"
							disabled={loading}
							onClick={() => {
								if (fighterId) void onLoadBackfill(fighterId);
							}}
						>
							{loading && <Loader2 className="w-3 h-3 mr-1 animate-spin" />}
							<span className="truncate">{buttonLabel}</span>
						</Button>
					)}
				</div>
			)}
		</div>
	);
}

function BackfillDot({
	status,
	loading,
}: {
	status: BackfillStatus | undefined;
	loading: boolean;
}) {
	if (loading) {
		return <Loader2 className="w-3 h-3 animate-spin text-muted-foreground" aria-label="Loading" />;
	}
	const color =
		status === 'current'
			? 'bg-emerald-500'
			: status === 'none' || status === 'failed'
				? 'bg-red-500'
				: status === 'stale_count' || status === 'stale_stats'
					? 'bg-yellow-500'
					: 'bg-muted-foreground';
	return (
		<span
			className={`size-2.5 rounded-full ${color}`}
			role="img"
			aria-label={status ?? 'loading'}
		/>
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

function resolveFightId(eventId: string, fightIndex: number, fight: FightCardEntry): string {
	if (fight.fightId) return fight.fightId;
	const [a, b] = fight.fighters;
	if (!a?.id || !b?.id) {
		return `ufcstats:pending-fight:${eventId}:${fightIndex}:tba`;
	}
	const pair = [a.id, b.id].sort().join('-vs-');
	return `ufcstats:pending-fight:${eventId}:${fightIndex}:${pair}`;
}

async function pollBackfillJob(
	jobId: string,
	fighterId: string,
	setJobProgress: React.Dispatch<React.SetStateAction<Record<string, string>>>,
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
