import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';

const outputPath = resolve('configs/experiments/market-grid-mass-edge-search.json');
const blendWeights = [null, 0.01, 0.05, 0.1, 0.25, 0.5];
const calibrations = [
	{ suffix: 'raw', value: undefined },
	{ suffix: 'temp125', value: { method: 'temperature', temperature: 1.25 } },
	{ suffix: 'temp150', value: { method: 'temperature', temperature: 1.5 } },
	{ suffix: 'temp200', value: { method: 'temperature', temperature: 2.0 } },
];

const xgboostParams = [
	['xgb_default', undefined],
	['xgb_shallow_slow', { n_estimators: 80, max_depth: 2, learning_rate: 0.03 }],
	['xgb_shallow', { n_estimators: 60, max_depth: 2, learning_rate: 0.05 }],
	['xgb_deeper_slow', { n_estimators: 80, max_depth: 4, learning_rate: 0.03 }],
	['xgb_more_trees', { n_estimators: 120, max_depth: 3, learning_rate: 0.03 }],
	[
		'xgb_sampled',
		{
			n_estimators: 80,
			max_depth: 3,
			learning_rate: 0.05,
			subsample: 0.75,
			colsample_bytree: 0.75,
		},
	],
];
const logisticParams = [
	['log_c025', { C: 0.25 }],
	['log_c050', { C: 0.5 }],
	['log_c100', undefined],
	['log_c200', { C: 2.0 }],
];

const featureSpecs = [
	['prod', 'production', undefined],
	['avail', 'production_plus_availability', undefined],
	['no_recent', 'production', { mode: 'exclude', names: ['recent_form'] }],
	['no_damage', 'production', { mode: 'exclude', names: ['damage'] }],
	['no_stance', 'production', { mode: 'exclude', names: ['stance'] }],
	['no_common', 'production', { mode: 'exclude', names: ['common_opponents'] }],
	[
		'core_stats',
		'production',
		{
			mode: 'only',
			names: [
				'slpm_diff',
				'str_acc_diff',
				'sapm_diff',
				'str_def_diff',
				'td_avg_diff',
				'td_acc_diff',
				'td_def_diff',
				'sub_avg_diff',
				'height_diff',
				'reach_diff',
				'age_diff',
			],
		},
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

for (const [featureSuffix, features, featureSubset] of featureSpecs) {
	for (const [paramSuffix, modelParams] of xgboostParams) {
		addVariantFamily({
			model: 'xgboost',
			prefix: `${paramSuffix}_${featureSuffix}`,
			features,
			featureSubset,
			modelParams,
			label: `${paramSuffix} ${featureSuffix}`,
		});
	}
	if (features === 'production') {
		for (const [paramSuffix, modelParams] of logisticParams) {
			addVariantFamily({
				model: 'logistic_regression',
				prefix: `${paramSuffix}_${featureSuffix}`,
				features,
				featureSubset,
				modelParams,
				label: `${paramSuffix} ${featureSuffix}`,
			});
		}
	}
}

function addVariantFamily({ model, prefix, features, featureSubset, modelParams, label }) {
	for (const calibration of calibrations) {
		for (const weight of blendWeights) {
			const parts = [prefix, calibration.suffix];
			if (weight !== null) {
				parts.push(`blend${String(Math.round(weight * 100)).padStart(2, '0')}`);
			}
			const variant = {
				name: parts.join('_'),
				model,
				features,
				market_blend_weight: weight,
				description: `${label} with ${calibration.suffix} calibration${weight === null ? '' : ` and ${Math.round(weight * 100)}% model blend`}.`,
			};
			if (modelParams !== undefined) {
				variant.model_params = modelParams;
			}
			if (featureSubset !== undefined) {
				variant.feature_subset = featureSubset;
			}
			if (calibration.value !== undefined) {
				variant.calibration = calibration.value;
			}
			variants.push(variant);
		}
	}
}

const names = new Set(variants.map((variant) => variant.name));
if (names.size !== variants.length) {
	throw new Error(`duplicate variant names: ${variants.length - names.size}`);
}

const config = {
	name: 'market-grid-mass-edge-search',
	description:
		'Mass report-only search across curated model hyperparameters, feature groups, deterministic calibration settings, and limited market blends.',
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
		json: 'data/experiments/harness/market-grid-mass-edge-search.json',
		markdown: 'data/experiments/harness/market-grid-mass-edge-search.md',
	},
};

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(config, null, 2)}\n`);
console.log(`Wrote ${outputPath} with ${variants.length} variants.`);
