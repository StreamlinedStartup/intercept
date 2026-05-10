import { Suspense } from 'react';
import { Skeleton } from '@/components/ui/skeleton';
import { UpcomingContent } from './upcoming-content';

export const metadata = {
	title: 'Upcoming Fights · UFC Stats',
	description: 'UFC fight cards in the next 7 days with side-by-side fighter stat comparisons.',
};

// Always render at request time so the "today" window reflects the user's clock.
export const dynamic = 'force-dynamic';

export default function UpcomingPage() {
	return (
		<Suspense fallback={<UpcomingPageSkeleton />}>
			<UpcomingContent />
		</Suspense>
	);
}

function UpcomingPageSkeleton() {
	return (
		<div className="flex flex-1 flex-col gap-6 max-w-5xl mx-auto w-full">
			<Skeleton className="h-10 w-72" />
			<Skeleton className="h-4 w-96" />
			<Skeleton className="h-64 w-full" />
			<Skeleton className="h-64 w-full" />
		</div>
	);
}
