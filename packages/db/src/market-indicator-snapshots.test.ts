import { describe, expect, it } from 'vitest';
import { marketIndicatorSnapshots } from './schema.js';

describe('market indicator snapshot schema', () => {
	it('materializes report-only market indicator probabilities and source metadata', () => {
		expect(marketIndicatorSnapshots.fightId.name).toBe('fight_id');
		expect(marketIndicatorSnapshots.target.name).toBe('target');
		expect(marketIndicatorSnapshots.modelVersion.name).toBe('model_version');
		expect(marketIndicatorSnapshots.indicatorName.name).toBe('indicator_name');
		expect(marketIndicatorSnapshots.computedAt.name).toBe('computed_at');
		expect(marketIndicatorSnapshots.modelProbability.name).toBe('model_probability');
		expect(marketIndicatorSnapshots.marketProbability.name).toBe('market_probability');
		expect(marketIndicatorSnapshots.edgePct.name).toBe('edge_pct');
		expect(marketIndicatorSnapshots.candidate.name).toBe('candidate');
		expect(marketIndicatorSnapshots.marketPairCount.name).toBe('market_pair_count');
		expect(marketIndicatorSnapshots.valueStatus.name).toBe('value_status');
		expect(marketIndicatorSnapshots.sourceReport.name).toBe('source_report');
		expect(marketIndicatorSnapshots.sourceConfig.name).toBe('source_config');
		expect(marketIndicatorSnapshots.sourceGitSha.name).toBe('source_git_sha');
		expect(marketIndicatorSnapshots.sourceModelPath.name).toBe('source_model_path');
		expect(marketIndicatorSnapshots.sourceDataWindow.name).toBe('source_data_window');
		expect(marketIndicatorSnapshots.stalenessReason.name).toBe('staleness_reason');
		expect(marketIndicatorSnapshots.rawMetadata.name).toBe('raw_metadata');
	});

	it('does not expose automated activation or betting columns', () => {
		expect('activated' in marketIndicatorSnapshots).toBe(false);
		expect('betSize' in marketIndicatorSnapshots).toBe(false);
		expect('wagerAmount' in marketIndicatorSnapshots).toBe(false);
		expect('placedAt' in marketIndicatorSnapshots).toBe(false);
	});
});
