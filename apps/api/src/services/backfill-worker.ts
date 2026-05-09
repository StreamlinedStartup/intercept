export type BackfillJobStatus = 'in_progress' | 'completed' | 'failed';

export type BackfillJobProgress = {
	current: number;
	total: number;
	message: string;
};

export type BackfillJob = {
	jobId: string;
	fighterId: string;
	status: BackfillJobStatus;
	progress: BackfillJobProgress;
	error: string | null;
	startedAt: string;
	completedAt: string | null;
};

type BackfillJobRunner = (controls: {
	setProgress: (progress: BackfillJobProgress) => void;
}) => Promise<void>;

const jobs = new Map<string, BackfillJob>();

export function startBackfillJob(fighterId: string, run: BackfillJobRunner): BackfillJob {
	const jobId = crypto.randomUUID();
	const job: BackfillJob = {
		jobId,
		fighterId,
		status: 'in_progress',
		progress: { current: 0, total: 0, message: 'Starting backfill' },
		error: null,
		startedAt: new Date().toISOString(),
		completedAt: null,
	};
	jobs.set(jobId, job);

	void run({
		setProgress: (progress) => {
			job.progress = progress;
		},
	})
		.then(() => {
			job.status = 'completed';
			job.completedAt = new Date().toISOString();
			if (!job.progress.message) {
				job.progress = { ...job.progress, message: 'Backfill complete' };
			}
		})
		.catch((err) => {
			job.status = 'failed';
			job.error = err instanceof Error ? err.message : String(err);
			job.completedAt = new Date().toISOString();
			job.progress = { ...job.progress, message: 'Backfill failed' };
		});

	return job;
}

export function getBackfillJob(jobId: string): BackfillJob | null {
	return jobs.get(jobId) ?? null;
}

export function serializeBackfillJob(job: BackfillJob) {
	return {
		job_id: job.jobId,
		fighter_id: job.fighterId,
		status: job.status,
		progress: job.progress,
		error: job.error,
		started_at: job.startedAt,
		completed_at: job.completedAt,
	};
}
