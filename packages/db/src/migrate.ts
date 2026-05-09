import { drizzle } from 'drizzle-orm/postgres-js';
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import postgres from 'postgres';

const url = process.env.DATABASE_URL;
if (!url) {
	console.error('DATABASE_URL is not set. Refusing to migrate without a database URL.');
	process.exit(1);
}

const client = postgres(url, { max: 1 });
const db = drizzle(client);

console.log(`[migrate] applying migrations to ${url.replace(/:[^@/]+@/, ':***@')}`);
await migrate(db, { migrationsFolder: 'migrations' });
console.log('[migrate] schema migrations applied');

const hypertables: Array<[string, string]> = [
	['fighter_stat_snapshots', 'snapshot_at'],
	['odds_snapshots', 'snapshot_at'],
	['predictions', 'predicted_at'],
];

for (const [table, column] of hypertables) {
	const rows = await client`
		SELECT create_hypertable(
			${table}::regclass,
			by_range(${column}::name),
			if_not_exists => TRUE,
			migrate_data => TRUE
		) AS result
	`;
	console.log(`[migrate] hypertable ${table}: ${JSON.stringify(rows[0])}`);
}

console.log('[migrate] done');
await client.end();
