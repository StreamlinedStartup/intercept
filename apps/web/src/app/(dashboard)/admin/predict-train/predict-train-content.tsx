'use client';

import { Loader2, Play } from 'lucide-react';
import type { ReactNode } from 'react';
import { useEffect, useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

type SeedResponse = {
	scope: 'in-window' | 'ppvs-5y';
	seed_job_id: string;
	window_days: number;
	event_count: number;
	fighter_count: number;
	queued_count: number;
	job?: SeedJob;
};

type SeedJob = {
	job_id: string;
	status: 'in_progress' | 'completed' | 'failed';
	progress: { current: number; total: number; message: string };
	error: string | null;
};

export function PredictTrainContent() {
	const [loadingScope, setLoadingScope] = useState<SeedResponse['scope'] | null>(null);
	const [error, setError] = useState<string | null>(null);
	const [result, setResult] = useState<SeedResponse | null>(null);
	const [job, setJob] = useState<SeedJob | null>(null);

	useEffect(() => {
		if (!result?.job || result.job.status !== 'in_progress') return;
		setJob(result.job);
		const timer = window.setInterval(async () => {
			const res = await fetch(`/api/predict/backfill/job/${result.job?.job_id}`);
			if (!res.ok) return;
			const next = (await res.json()) as SeedJob;
			setJob(next);
			if (next.status !== 'in_progress') window.clearInterval(timer);
		}, 1500);
		return () => window.clearInterval(timer);
	}, [result]);

	async function seed(scope: SeedResponse['scope']) {
		setLoadingScope(scope);
		setError(null);
		setResult(null);
		setJob(null);
		try {
			const res = await fetch(`/api/predict/backfill/seed?scope=${scope}`, { method: 'POST' });
			if (!res.ok) {
				const text = await res.text();
				throw new Error(`Seed request returned ${res.status}: ${text.slice(0, 200)}`);
			}
			setResult((await res.json()) as SeedResponse);
		} catch (err) {
			setError(err instanceof Error ? err.message : String(err));
		} finally {
			setLoadingScope(null);
		}
	}

	return (
		<div className="flex flex-1 flex-col gap-6 max-w-3xl mx-auto w-full">
			<header className="flex flex-col gap-1">
				<h1 className="text-2xl sm:text-3xl font-bold tracking-tight">Predictor Training</h1>
				<p className="text-sm text-muted-foreground">Seed fighter history for upcoming cards.</p>
			</header>

			<Card>
				<CardHeader className="flex flex-row items-center justify-between gap-3">
					<div>
						<CardTitle className="text-base">In-window seed</CardTitle>
						<p className="text-sm text-muted-foreground mt-1">
							Queue fighters from UFC cards in the next 30 days.
						</p>
					</div>
					<Badge variant="outline">30 days</Badge>
				</CardHeader>
				<CardContent className="flex flex-col gap-4">
					<div className="flex flex-wrap gap-2">
						<SeedButton
							loading={loadingScope === 'in-window'}
							disabled={loadingScope !== null}
							onClick={() => seed('in-window')}
						>
							Seed: in-window
						</SeedButton>
						<SeedButton
							loading={loadingScope === 'ppvs-5y'}
							disabled={loadingScope !== null}
							onClick={() => seed('ppvs-5y')}
						>
							Seed: PPVs (5y)
						</SeedButton>
					</div>

					{error && (
						<Alert variant="destructive">
							<AlertDescription>{error}</AlertDescription>
						</Alert>
					)}

					{result && (
						<>
							<div className="grid grid-cols-3 gap-3 text-sm">
								<Metric label="Events" value={result.event_count} />
								<Metric label="Fighters" value={result.fighter_count} />
								<Metric label="Queued" value={result.queued_count} />
							</div>
							{job && (
								<div className="rounded-md border border-border/60 px-3 py-2 text-sm">
									<div className="flex items-center justify-between gap-3">
										<span className="text-muted-foreground">{job.progress.message}</span>
										<Badge variant="outline">{job.status}</Badge>
									</div>
									<div className="mt-1 tabular-nums">
										{job.progress.current} / {job.progress.total}
									</div>
								</div>
							)}
						</>
					)}
				</CardContent>
			</Card>
		</div>
	);
}

function SeedButton({
	children,
	disabled,
	loading,
	onClick,
}: {
	children: ReactNode;
	disabled: boolean;
	loading: boolean;
	onClick: () => void;
}) {
	return (
		<Button type="button" className="w-fit" disabled={disabled} onClick={onClick}>
			{loading ? (
				<Loader2 className="w-4 h-4 mr-2 animate-spin" />
			) : (
				<Play className="w-4 h-4 mr-2" />
			)}
			{children}
		</Button>
	);
}

function Metric({ label, value }: { label: string; value: number }) {
	return (
		<div className="rounded-md border border-border/60 px-3 py-2">
			<div className="text-xs text-muted-foreground">{label}</div>
			<div className="text-xl font-semibold tabular-nums">{value}</div>
		</div>
	);
}
