import { describe, expect, it } from 'vitest';
import { buildMlPredictParams } from './predict';

describe('buildMlPredictParams', () => {
	it('forwards target fight weight class to ml.predict', () => {
		expect(
			buildMlPredictParams(
				{
					event_date: new Date('2026-06-01T12:00:00.000Z'),
					weight_class: 'Welterweight',
					fighter_id: 'fighter-a',
				},
				{ fighter_id: 'fighter-b' },
			),
		).toEqual({
			fighter_a_id: 'fighter-a',
			fighter_b_id: 'fighter-b',
			fight_date: '2026-06-01',
			weight_class: 'Welterweight',
		});
	});
});
