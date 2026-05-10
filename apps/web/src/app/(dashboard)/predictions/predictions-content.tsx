'use client';

import { Check, RefreshCw, X } from 'lucide-react';
import { useCallback, useEffect, useState } from 'react';
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

export function PredictionsContent() {
	const [history, setHistory] = useState<HistoryResponse | null>(null);
	const [model, setModel] = useState<LatestModel>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

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
					<PredictionsTable rows={history.rows} />
				</>
			) : (
				<EmptyState />
			)}
		</div>
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
