'use client';

import { Check, RefreshCw, X } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from '@/components/ui/table';

type HistoryResponse = {
	aggregate: {
		n_predictions: number;
		n_with_result: number;
		accuracy: number | null;
		log_loss: number | null;
		brier: number | null;
		n_bets: number;
		roi_units: number;
		roi_pct: number | null;
	};
	rows: HistoryRow[];
};

type HistoryRow = {
	fight_id: string;
	event_name: string;
	event_date: string;
	predicted_at: string;
	predicted_winner_id: string;
	predicted_winner_name: string;
	win_prob: number;
	market_prob: number | null;
	edge_pct: number | null;
	actual_winner_id: string | null;
	actual_winner_name: string | null;
	hit: boolean | null;
	bet_pl_units: number | null;
};

type ModelListResponse = {
	result: {
		models: Array<{
			id: string;
			trained_at: string;
			accuracy: number | null;
			log_loss: number | null;
			brier_score: number | null;
		}>;
	};
};

type LatestModel = ModelListResponse['result']['models'][number] | null;
type RoiFilter = 'all' | 'edge5' | 'edge10';

const ROI_FILTERS: Array<{ label: string; value: RoiFilter; minEdge: number }> = [
	{ label: 'All', value: 'all', minEdge: Number.NEGATIVE_INFINITY },
	{ label: 'Edge >5%', value: 'edge5', minEdge: 0.05 },
	{ label: 'Edge >10%', value: 'edge10', minEdge: 0.1 },
];

export function PredictionsContent() {
	const [history, setHistory] = useState<HistoryResponse | null>(null);
	const [model, setModel] = useState<LatestModel>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const [roiFilter, setRoiFilter] = useState<RoiFilter>('all');

	const load = useCallback(async () => {
		setLoading(true);
		setError(null);
		try {
			const [historyRes, modelRes] = await Promise.all([
				fetch('/api/predict/history?limit=50'),
				fetch('/api/python/ml.list_models', {
					method: 'POST',
					headers: { 'content-type': 'application/json' },
					body: JSON.stringify({ limit: 1 }),
				}),
			]);
			if (!historyRes.ok) {
				throw new Error(`Prediction history returned ${historyRes.status}`);
			}
			if (!modelRes.ok) {
				throw new Error(`Model list returned ${modelRes.status}`);
			}
			const historyBody = (await historyRes.json()) as HistoryResponse;
			const modelBody = (await modelRes.json()) as ModelListResponse;
			setHistory(historyBody);
			setModel(modelBody.result.models[0] ?? null);
		} catch (err) {
			setError(err instanceof Error ? err.message : String(err));
		} finally {
			setLoading(false);
		}
	}, []);

	useEffect(() => {
		void load();
	}, [load]);

	return (
		<div className="flex flex-1 flex-col gap-6 max-w-6xl mx-auto w-full">
			<header className="flex flex-col gap-1">
				<div className="flex items-center justify-between gap-3">
					<h1 className="text-2xl sm:text-3xl font-bold tracking-tight">Predictions</h1>
					<Button
						type="button"
						variant="outline"
						size="sm"
						onClick={() => void load()}
						disabled={loading}
					>
						<RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
						<span className="hidden sm:inline ml-1.5">Refresh</span>
					</Button>
				</div>
				<p className="text-sm text-muted-foreground">Model track record and recent picks.</p>
			</header>

			{error && (
				<Alert variant="destructive">
					<AlertDescription>{error}</AlertDescription>
				</Alert>
			)}

			{loading ? (
				<PredictionsSkeleton />
			) : history && history.rows.length > 0 ? (
				<>
					<MetricsGrid model={model} history={history} />
					<RoiChart rows={history.rows} filter={roiFilter} onFilterChange={setRoiFilter} />
					<PredictionsTable rows={history.rows} />
				</>
			) : (
				<EmptyState />
			)}
		</div>
	);
}

function RoiChart({
	rows,
	filter,
	onFilterChange,
}: {
	rows: HistoryRow[];
	filter: RoiFilter;
	onFilterChange: (filter: RoiFilter) => void;
}) {
	const points = useMemo(() => buildRoiSeries(rows, filter), [rows, filter]);
	const chart = buildRoiChart(points);

	return (
		<Card>
			<CardHeader className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
				<CardTitle className="text-base">Cumulative ROI</CardTitle>
				<div className="flex rounded-md border p-1 w-fit">
					{ROI_FILTERS.map((option) => (
						<Button
							key={option.value}
							type="button"
							size="sm"
							variant={filter === option.value ? 'secondary' : 'ghost'}
							className="h-7 px-2 text-xs"
							onClick={() => onFilterChange(option.value)}
						>
							{option.label}
						</Button>
					))}
				</div>
			</CardHeader>
			<CardContent>
				{chart ? (
					<div className="h-72 w-full">
						<svg className="h-full w-full overflow-visible" viewBox="0 0 640 260" role="img">
							<title>Cumulative betting units by event date</title>
							<line
								x1={40}
								x2={620}
								y1={chart.zeroY}
								y2={chart.zeroY}
								stroke="currentColor"
								strokeDasharray="4 4"
								className="text-muted-foreground/70"
							/>
							<text
								x={44}
								y={Math.max(14, chart.zeroY - 8)}
								className="fill-muted-foreground text-[10px]"
							>
								breakeven
							</text>
							<polyline
								points={chart.path}
								fill="none"
								stroke="currentColor"
								strokeWidth="3"
								strokeLinejoin="round"
								strokeLinecap="round"
								className="text-emerald-600"
							/>
							{chart.points.map((point) => (
								<circle
									key={point.key}
									cx={point.x}
									cy={point.y}
									r="4"
									className="fill-background stroke-emerald-600"
									strokeWidth="2"
								>
									<title>
										{point.label}: {formatSignedNumber(point.units)} units
									</title>
								</circle>
							))}
							<text x={40} y={252} className="fill-muted-foreground text-[10px]">
								{chart.firstLabel}
							</text>
							<text x={620} y={252} textAnchor="end" className="fill-muted-foreground text-[10px]">
								{chart.lastLabel}
							</text>
							<text x={40} y={18} className="fill-muted-foreground text-[10px]">
								{formatSignedNumber(chart.maxUnits)}u
							</text>
							<text x={40} y={238} className="fill-muted-foreground text-[10px]">
								{formatSignedNumber(chart.minUnits)}u
							</text>
						</svg>
					</div>
				) : (
					<div className="h-40 flex items-center justify-center rounded-md border border-dashed text-sm text-muted-foreground">
						No resolved bets for this filter
					</div>
				)}
			</CardContent>
		</Card>
	);
}

function MetricsGrid({ model, history }: { model: LatestModel; history: HistoryResponse }) {
	const aggregate = history.aggregate;
	return (
		<div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
			<Metric label="Model" value={model?.id ?? 'None'} compact />
			<Metric label="Trained" value={model ? formatDate(model.trained_at) : 'None'} />
			<Metric label="Log loss" value={formatNumber(model?.log_loss ?? aggregate.log_loss)} />
			<Metric label="Brier" value={formatNumber(model?.brier_score ?? aggregate.brier)} />
			<Metric label="Accuracy" value={formatPercent(model?.accuracy ?? aggregate.accuracy)} />
			<Metric label="Predictions" value={aggregate.n_predictions} />
			<Metric label="With result" value={aggregate.n_with_result} />
			<Metric label="Bets" value={aggregate.n_bets} />
			<Metric label="ROI units" value={formatSignedNumber(aggregate.roi_units)} />
			<Metric label="ROI" value={formatPercent(aggregate.roi_pct)} />
		</div>
	);
}

function Metric({
	label,
	value,
	compact = false,
}: {
	label: string;
	value: string | number;
	compact?: boolean;
}) {
	return (
		<Card>
			<CardContent className="px-3 py-3">
				<div className="text-xs text-muted-foreground">{label}</div>
				<div className={`font-semibold tabular-nums ${compact ? 'text-xs truncate' : 'text-xl'}`}>
					{value}
				</div>
			</CardContent>
		</Card>
	);
}

function PredictionsTable({ rows }: { rows: HistoryRow[] }) {
	return (
		<Card>
			<CardHeader>
				<CardTitle className="text-base">Last 50 Predictions</CardTitle>
			</CardHeader>
			<CardContent>
				<div className="rounded-md border overflow-x-auto">
					<Table>
						<TableHeader>
							<TableRow>
								<TableHead>Date</TableHead>
								<TableHead>Fighter</TableHead>
								<TableHead>Pick</TableHead>
								<TableHead className="text-right">WinProb</TableHead>
								<TableHead className="text-right">Vegas</TableHead>
								<TableHead>Result</TableHead>
								<TableHead className="text-center">Hit</TableHead>
							</TableRow>
						</TableHeader>
						<TableBody>
							{rows.map((row) => (
								<TableRow key={`${row.fight_id}-${row.predicted_at}`}>
									<TableCell className="whitespace-nowrap">{formatDate(row.event_date)}</TableCell>
									<TableCell className="min-w-44">
										<div className="font-medium">{row.predicted_winner_name}</div>
										<div className="text-xs text-muted-foreground truncate max-w-56">
											{row.event_name}
										</div>
									</TableCell>
									<TableCell>
										<Badge variant="secondary">{row.predicted_winner_name}</Badge>
									</TableCell>
									<TableCell className="text-right tabular-nums">
										{formatPercent(row.win_prob)}
									</TableCell>
									<TableCell className="text-right tabular-nums">
										{formatPercent(row.market_prob)}
									</TableCell>
									<TableCell>
										{row.actual_winner_name ? (
											<span>{row.actual_winner_name}</span>
										) : (
											<span className="text-muted-foreground">Pending</span>
										)}
									</TableCell>
									<TableCell className="text-center">
										<HitIcon hit={row.hit} />
									</TableCell>
								</TableRow>
							))}
						</TableBody>
					</Table>
				</div>
			</CardContent>
		</Card>
	);
}

function buildRoiSeries(rows: HistoryRow[], filter: RoiFilter) {
	const selectedFilter = ROI_FILTERS.find((option) => option.value === filter) ?? ROI_FILTERS[0];
	let cumulativeUnits = 0;

	return rows
		.filter((row) => row.hit !== null && row.market_prob !== null)
		.filter((row) => (row.edge_pct ?? Number.NEGATIVE_INFINITY) > selectedFilter.minEdge)
		.toSorted((a, b) => {
			const eventDateDiff = a.event_date.localeCompare(b.event_date);
			if (eventDateDiff !== 0) return eventDateDiff;
			return a.predicted_at.localeCompare(b.predicted_at);
		})
		.map((row) => {
			const units = typeof row.bet_pl_units === 'number' ? row.bet_pl_units : estimateBetUnits(row);
			cumulativeUnits += units;
			return {
				key: `${row.fight_id}-${row.predicted_at}`,
				label: formatDate(row.event_date),
				units: cumulativeUnits,
			};
		});
}

function buildRoiChart(points: ReturnType<typeof buildRoiSeries>) {
	if (points.length === 0) return null;

	const width = 640;
	const height = 260;
	const left = 40;
	const right = 620;
	const top = 18;
	const bottom = 230;
	const units = points.map((point) => point.units);
	const minUnits = Math.min(0, ...units);
	const maxUnits = Math.max(0, ...units);
	const range = maxUnits - minUnits || 1;

	const plottedPoints = points.map((point, index) => {
		const x =
			points.length === 1
				? (left + right) / 2
				: left + (index / (points.length - 1)) * (right - left);
		const y = bottom - ((point.units - minUnits) / range) * (bottom - top);
		return { ...point, x, y };
	});

	const zeroY = bottom - ((0 - minUnits) / range) * (bottom - top);
	return {
		width,
		height,
		path: plottedPoints.map((point) => `${point.x.toFixed(1)},${point.y.toFixed(1)}`).join(' '),
		points: plottedPoints,
		zeroY,
		minUnits,
		maxUnits,
		firstLabel: points[0]?.label ?? '',
		lastLabel: points.at(-1)?.label ?? '',
	};
}

function estimateBetUnits(row: HistoryRow): number {
	if (row.hit === false) return -1;
	if (row.hit === true && row.market_prob && row.market_prob > 0) return 1 / row.market_prob - 1;
	return 0;
}

function HitIcon({ hit }: { hit: boolean | null }) {
	if (hit === null) return <span className="text-muted-foreground">-</span>;
	if (hit) return <Check className="w-4 h-4 mx-auto text-emerald-600" aria-label="Hit" />;
	return <X className="w-4 h-4 mx-auto text-destructive" aria-label="Miss" />;
}

function EmptyState() {
	return (
		<Card className="border-dashed">
			<CardContent className="py-14 text-center">
				<div className="text-base font-medium">No predictions yet</div>
				<p className="text-sm text-muted-foreground mt-1">
					Prediction history appears after fight predictions are generated.
				</p>
			</CardContent>
		</Card>
	);
}

function PredictionsSkeleton() {
	const skeletonKeys = [
		'model',
		'trained',
		'log-loss',
		'brier',
		'accuracy',
		'predictions',
		'with-results',
		'roi',
		'calibration',
		'market',
	];

	return (
		<div className="flex flex-col gap-4">
			<div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
				{skeletonKeys.map((key) => (
					<Skeleton key={key} className="h-20" />
				))}
			</div>
			<Skeleton className="h-96" />
		</div>
	);
}

function formatDate(value: string): string {
	const date = new Date(value);
	if (Number.isNaN(date.getTime())) return value.slice(0, 10);
	return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatNumber(value: number | null | undefined): string {
	return typeof value === 'number' ? value.toFixed(3) : '-';
}

function formatSignedNumber(value: number | null | undefined): string {
	if (typeof value !== 'number') return '-';
	return `${value > 0 ? '+' : ''}${value.toFixed(2)}`;
}

function formatPercent(value: number | null | undefined): string {
	return typeof value === 'number' ? `${Math.round(value * 100)}%` : '-';
}
