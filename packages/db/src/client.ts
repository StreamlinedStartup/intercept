import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema.js';

const url = process.env.DATABASE_URL;
if (!url) {
	throw new Error(
		'DATABASE_URL is not set. Refusing to start without a database connection. ' +
			'Set DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor (see docker-compose.yml).',
	);
}

export const sql = postgres(url, { max: 10 });
export const db = drizzle(sql, { schema });

export type Database = typeof db;
