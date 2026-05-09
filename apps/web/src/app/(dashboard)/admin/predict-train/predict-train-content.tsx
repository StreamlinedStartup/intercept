'use client';

import { Loader2, Play } from 'lucide-react';
import { useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

type SeedResponse = {
	scope: 'in-window';
	seed_job_id: string;
	window_days: number;
	event_count: number;
	fighter_count: number;
	queued_count: number;
};

export function PredictTrainContent() {
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [result, setResult] = useState<SeedResponse | null>(null);

	async function seedInWindow() {
		setLoading(true);
		setError(null);
		setResult(null);
		try {
			const res = await fetch('/api/predict/backfill/seed?scope=in-window', { method: 'POST' });
			if (!res.ok) {
				const text = await res.text();
				throw new Error(`Seed request returned ${res.status}: ${text.slice(0, 200)}`);
			}
			setResult((await res.json()) as SeedResponse);
		} catch (err) {
			setError(err instanceof Error ? err.message : String(err));
		} finally {
			setLoading(false);
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
					<Button type="button" className="w-fit" disabled={loading} onClick={seedInWindow}>
						{loading ? (
							<Loader2 className="w-4 h-4 mr-2 animate-spin" />
						) : (
							<Play className="w-4 h-4 mr-2" />
						)}
						Seed: in-window
					</Button>

					{error && (
						<Alert variant="destructive">
							<AlertDescription>{error}</AlertDescription>
						</Alert>
					)}

					{result && (
						<div className="grid grid-cols-3 gap-3 text-sm">
							<Metric label="Events" value={result.event_count} />
							<Metric label="Fighters" value={result.fighter_count} />
							<Metric label="Queued" value={result.queued_count} />
						</div>
					)}
				</CardContent>
			</Card>
		</div>
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
