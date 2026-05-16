import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';

const outputPath = resolve('configs/experiments/market-grid-expanded-100.json');
const weights = Array.from({ length: 33 }, (_, index) =>
	Number(((index * 3 + 1) / 100).toFixed(2)),
);

const families = [
	['xgb_prod', 'xgboost', 'production', 'XGBoost production features'],
	[
		'xgb_avail',
		'xgboost',
		'production_plus_availability',
		'XGBoost with feature availability indicators',
	],
	[
		'log_prod',
		'logistic_regression',
		'production',
		'regularized logistic regression production features',
	],
];

const variants = [
	{
		name: 'market_favorite',
		model: 'market_favorite',
		features: 'none',
		market_blend_weight: null,
		description: 'No-vig market favorite baseline.',
	},
];

for (const [prefix, model, features, label] of families) {
	variants.push({
		name: `${prefix}_unblended`,
		model,
		features,
		market_blend_weight: null,
		description: `${label} without market blending.`,
	});

	for (const weight of weights) {
		const modelPct = Math.round(weight * 100);
		const marketPct = Math.round((1 - weight) * 100);
		variants.push({
			name: `${prefix}_blend_${String(modelPct).padStart(2, '0')}_model_${String(marketPct).padStart(2, '0')}_market`,
			model,
			features,
			market_blend_weight: weight,
			description: `${modelPct}% ${label} probability plus ${marketPct}% no-vig market probability.`,
		});
	}
}

const config = {
	name: 'market-grid-expanded-100',
	description:
		'Expanded report-only matrix for dense model-to-market blend sweeps across production XGBoost, availability-augmented XGBoost, and logistic regression.',
	value_status: 'research_only',
	report_only: true,
	writes_model_versions: false,
	corpus: {
		source: 'matched_market_fights',
		market_source: 'fightodds_no_vig_consensus',
		min_train_samples: 100,
		max_events: null,
	},
	split: {
		policy: 'chronological_walk_forward',
		candidate_selection: 'full_current_corpus',
		locked_evaluation: 'future_required',
	},
	gate: {
		baseline: 'market_favorite',
		min_roi_delta_vs_market: 0.02,
		probability_quality: {
			require_log_loss_not_worse: true,
			require_brier_not_worse: true,
		},
	},
	variants,
	outputs: {
		json: 'data/experiments/harness/market-grid-expanded-100.json',
		markdown: 'data/experiments/harness/market-grid-expanded-100.md',
	},
};

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(config, null, 2)}\n`);
console.log(`Wrote ${outputPath} with ${variants.length} variants.`);
