import type { Config } from 'drizzle-kit';

export default {
	schema: './src/schema.ts',
	out: './migrations',
	dialect: 'postgresql',
	dbCredentials: {
		url:
			process.env.DATABASE_URL ?? 'postgres://interceptor:interceptor@localhost:5434/interceptor',
	},
} satisfies Config;
