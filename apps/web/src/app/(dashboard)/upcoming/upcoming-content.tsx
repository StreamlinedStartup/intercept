'use client';

import { CalendarRange, MapPin, RefreshCw } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { DEBUG } from '@/lib/debug';
import { CompareSheet } from './compare-sheet';
import { EventFightCard } from './event-fight-card';
import {
	type EventDetail,
	friendlyDate,
	isInWindow,
	parseUfcDate,
	type UpcomingEvent,
	type UpcomingResponse,
} from './upcoming-types';

const WINDOW_DAYS = 7;

type EventState = {
	meta: UpcomingEvent;
	detail: EventDetail | null;
	loading: boolean;
	error: string | null;
};

type CompareTarget = {
	fightId: string;
	fighterA: { id: string; name: string };
	fighterB: { id: string; name: string };
	weightClass: string;
	eventName: string;
} | null;

export function UpcomingContent() {
	const today = useMemo(() => new Date(), []);
	const windowEnd = useMemo(() => {
		const e = new Date(today);
		e.setDate(e.getDate() + WINDOW_DAYS);
		return e;
	}, [today]);

	const [upcomingError, setUpcomingError] = useState<string | null>(null);
	const [upcomingLoading, setUpcomingLoading] = useState(true);
	const [events, setEvents] = useState<EventState[]>([]);
	const [compare, setCompare] = useState<CompareTarget>(null);

	const loadEvents = useCallback(async () => {
		setUpcomingLoading(true);
		setUpcomingError(null);
		setEvents([]);
		DEBUG('upcoming', () => `fetch-upcoming today=${today.toISOString()}`);
		try {
			const res = await fetch('/api/ufcstats/events/upcoming');
			if (!res.ok) {
				throw new Error(`Upcoming events list returned ${res.status}`);
			}
			const data = (await res.json()) as UpcomingResponse;
			DEBUG('upcoming', () => `upcoming-loaded total=${data.events.length}`);

			const inWindow = data.events.filter((e) => {
				const d = parseUfcDate(e.date);
				return d ? isInWindow(d, today, WINDOW_DAYS) : false;
			});
			DEBUG(
				'upcoming',
				() =>
					`window-filter kept=${inWindow.length} dropped=${data.events.length - inWindow.length}`,
			);

			const initial: EventState[] = inWindow.map((meta) => ({
				meta,
				detail: null,
				loading: true,
				error: null,
			}));
			setEvents(initial);
			setUpcomingLoading(false);

			// Fetch event details sequentially to be a polite citizen on
			// ufcstats.com (rate-limited at 30/min in api/register-domains).
			for (let i = 0; i < initial.length; i++) {
				const ev = initial[i];
				try {
					DEBUG('upcoming', () => `fetch-event-detail id=${ev.meta.id}`);
					const er = await fetch(`/api/ufcstats/event/${ev.meta.id}`);
					if (!er.ok) throw new Error(`Event detail ${ev.meta.id} returned ${er.status}`);
					const detail = (await er.json()) as EventDetail;
					setEvents((prev) =>
						prev.map((p, idx) => (idx === i ? { ...p, detail, loading: false } : p)),
					);
				} catch (err) {
					const msg = err instanceof Error ? err.message : 'unknown error';
					DEBUG('upcoming', () => `event-detail-failed id=${ev.meta.id} msg=${msg}`);
					setEvents((prev) =>
						prev.map((p, idx) => (idx === i ? { ...p, error: msg, loading: false } : p)),
					);
				}
			}
		} catch (err) {
			const msg = err instanceof Error ? err.message : 'Failed to load events';
			DEBUG('upcoming', () => `upcoming-failed msg=${msg}`);
			setUpcomingError(msg);
			setUpcomingLoading(false);
		}
	}, [today]);

	useEffect(() => {
		void loadEvents();
	}, [loadEvents]);

	const headerSubtitle = `${today.toLocaleDateString('en-US', {
		month: 'short',
		day: 'numeric',
	})} — ${windowEnd.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;

	return (
		<div className="flex flex-1 flex-col gap-6 max-w-5xl mx-auto w-full">
			<header className="flex flex-col gap-1">
				<div className="flex items-center justify-between gap-2">
					<h1 className="text-2xl sm:text-3xl font-bold tracking-tight">This Week's Fights</h1>
					<Button
						variant="outline"
						size="sm"
						onClick={() => void loadEvents()}
						disabled={upcomingLoading}
						aria-label="Refresh upcoming events"
					>
						<RefreshCw className={`w-4 h-4 ${upcomingLoading ? 'animate-spin' : ''}`} />
						<span className="hidden sm:inline ml-1.5">Refresh</span>
					</Button>
				</div>
				<p className="text-sm text-muted-foreground flex items-center gap-1.5">
					<CalendarRange className="w-4 h-4" />
					Next {WINDOW_DAYS} days · {headerSubtitle}
				</p>
			</header>

			{upcomingError && (
				<Alert variant="destructive">
					<AlertDescription>
						Couldn't load upcoming events — {upcomingError}.{' '}
						<button
							type="button"
							className="underline underline-offset-2 hover:no-underline"
							onClick={() => void loadEvents()}
						>
							Try again
						</button>
					</AlertDescription>
				</Alert>
			)}

			{upcomingLoading && <UpcomingSkeleton />}

			{!upcomingLoading && !upcomingError && events.length === 0 && (
				<EmptyState today={today} windowEnd={windowEnd} />
			)}

			{!upcomingLoading && events.length > 0 && (
				<div className="flex flex-col gap-6">
					{events.map((ev) => (
						<EventBlock
							key={ev.meta.id}
							ev={ev}
							today={today}
							onCompare={(fightId, fighterA, fighterB, weightClass) =>
								setCompare({ fightId, fighterA, fighterB, weightClass, eventName: ev.meta.name })
							}
						/>
					))}
				</div>
			)}

			<CompareSheet
				key={compare ? `${compare.fighterA.id}-${compare.fighterB.id}` : 'closed'}
				target={compare}
				today={today}
				onClose={() => setCompare(null)}
			/>
		</div>
	);
}

function UpcomingSkeleton() {
	return (
		<div className="flex flex-col gap-6">
			{[0, 1].map((i) => (
				<Card key={i}>
					<CardHeader className="space-y-2">
						<Skeleton className="h-7 w-2/3" />
						<Skeleton className="h-4 w-1/2" />
					</CardHeader>
					<CardContent>
						<div className="space-y-2">
							{[0, 1, 2, 3].map((j) => (
								<Skeleton key={j} className="h-14 w-full" />
							))}
						</div>
					</CardContent>
				</Card>
			))}
		</div>
	);
}

function EmptyState({ today, windowEnd }: { today: Date; windowEnd: Date }) {
	return (
		<Card className="border-dashed">
			<CardContent className="flex flex-col items-center justify-center text-center gap-3 py-14">
				<div className="w-16 h-16 rounded-2xl bg-muted/50 flex items-center justify-center">
					<CalendarRange className="w-8 h-8 text-muted-foreground" />
				</div>
				<div className="text-base font-medium">No fights in the next 7 days</div>
				<p className="text-sm text-muted-foreground max-w-sm">
					Nothing on the UFC calendar between{' '}
					<span className="font-medium text-foreground">
						{today.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
					</span>{' '}
					and{' '}
					<span className="font-medium text-foreground">
						{windowEnd.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
					</span>
					. Check back closer to the next event.
				</p>
			</CardContent>
		</Card>
	);
}

function EventBlock({
	ev,
	today,
	onCompare,
}: {
	ev: EventState;
	today: Date;
	onCompare: (
		fightId: string,
		a: { id: string; name: string },
		b: { id: string; name: string },
		weightClass: string,
	) => void;
}) {
	const eventDate = parseUfcDate(ev.meta.date);
	const friendly = eventDate ? friendlyDate(eventDate, today) : ev.meta.date;
	const isToday = friendly === 'Today';

	return (
		<Card className="overflow-hidden">
			<CardHeader className="space-y-2">
				<div className="flex items-start justify-between gap-3 flex-wrap">
					<CardTitle className="text-xl sm:text-2xl">{ev.meta.name}</CardTitle>
					<Badge
						variant={isToday ? 'default' : 'secondary'}
						className={isToday ? 'bg-red-600 hover:bg-red-600 text-white' : ''}
					>
						{friendly.toUpperCase()}
					</Badge>
				</div>
				<div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
					<span className="flex items-center gap-1.5">
						<CalendarRange className="w-4 h-4" />
						{ev.meta.date}
					</span>
					<span className="flex items-center gap-1.5">
						<MapPin className="w-4 h-4" />
						{ev.meta.location}
					</span>
				</div>
			</CardHeader>
			<CardContent>
				{ev.loading && <FightListSkeleton />}
				{ev.error && (
					<Alert variant="destructive">
						<AlertDescription>
							Couldn't load fight card for {ev.meta.name} — {ev.error}.
						</AlertDescription>
					</Alert>
				)}
				{!ev.loading && !ev.error && ev.detail && (
					<EventFightCard detail={ev.detail} onCompare={onCompare} />
				)}
			</CardContent>
		</Card>
	);
}

function FightListSkeleton() {
	return (
		<div className="space-y-2">
			{[0, 1, 2, 3].map((i) => (
				<Skeleton key={i} className="h-14 w-full" />
			))}
		</div>
	);
}
