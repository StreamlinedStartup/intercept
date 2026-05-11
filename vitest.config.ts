import { defineConfig } from 'vitest/config';

export default defineConfig({
	test: {
		watch: false,
		projects: ['packages/shared', 'packages/browser', 'packages/db', 'apps/api', 'apps/web'],
	},
});
