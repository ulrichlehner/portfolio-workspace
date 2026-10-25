import copy
from decimal import Decimal
import unittest

from compare_fund_holdings import compare


class FundComparisonTest(unittest.TestCase):
    def setUp(self):
        self.provider = [dict(isin='SYNTHETIC-ONE', name='Invented equity', percent='99.9', value='999',
                              assetType=None, updated_at='2026-01-03T00:00:00Z')]
        values = dict(isin=['SYNTHETIC-ONE', '-', '-'], issueName=['Different display label', 'Synthetic cash',
                                                                 'Synthetic future'],
                      holdingPercent=['99.90000', '0.10000', '0.00000'],
                      marketValue=['999', '1', '0'], notionalValue=['999', '1', '50'],
                      assetClass=['Equity', 'Cash', 'Futures'])
        self.points = {key: dict(value=value) for key, value in values.items()}
        self.points['asOfDate'] = dict(value=20260102)
        self.issuer = dict(currencyCode='USD', componentsByNameMap=dict(holdings=dict(
            containersByNameMap=dict(all=dict(dataPointsByNameMap=self.points)))))

    def test_exact_isin_matching_not_label_or_update_date(self):
        result = compare(self.provider, self.issuer)
        self.assertEqual(1, result['isin_matched_rows'])
        self.assertEqual('20260102', result['issuer_effective_date'])
        self.assertIsNone(result['provider_holdings_effective_date'])
        self.assertEqual(Decimal('0'), result['weight_difference_pp']['maximum'])

    def test_zero_value_derivatives_are_not_dropped(self):
        result = compare(self.provider, self.issuer)
        self.assertEqual(1, len(result['zero_value_positive_notional_rows']))
        self.assertEqual(Decimal('50'), result['issuer_asset_classes']['Futures']['notional_value'])
        self.assertFalse(result['validated_complete_economic_exposure'])

    def test_missing_isin_name_candidate_does_not_become_verified(self):
        self.provider.append(dict(isin=None, name='Synthetic cash', percent='0.1', value='1'))
        result = compare(self.provider, self.issuer)
        self.assertEqual(1, result['isin_matched_rows'])
        self.assertEqual(1, len(result['identifierless_name_candidates']))
        self.assertEqual(1, len(result['unmatched_provider_rows']))

    def test_duplicate_rows_are_preserved_not_merged(self):
        self.provider.append(copy.deepcopy(self.provider[0]))
        result = compare(self.provider, self.issuer)
        self.assertEqual(0, result['isin_matched_rows'])
        self.assertEqual({'SYNTHETIC-ONE': 2}, result['duplicate_provider_isins'])
        self.assertEqual(2, len(result['unmatched_provider_rows']))

    def test_mismatched_parallel_arrays_fail_closed(self):
        self.points['isin']['value'].pop()
        with self.assertRaises(ValueError):
            compare(self.provider, self.issuer)

    def test_missing_effective_date_is_not_replaced(self):
        del self.points['asOfDate']
        with self.assertRaises(KeyError):
            compare(self.provider, self.issuer)

    def test_nonfinite_weight_is_rejected(self):
        self.provider[0]['percent'] = 'NaN'
        with self.assertRaises(ValueError):
            compare(self.provider, self.issuer)

    def test_small_source_difference_is_compared_to_raw_rounding(self):
        self.provider[0]['percent'] = '99.90000001'
        result = compare(self.provider, self.issuer)
        self.assertEqual(1, result['isin_matches_within_rounding'])
        self.provider[0]['percent'] = '99.91'
        self.assertEqual(0, compare(self.provider, self.issuer)['isin_matches_within_rounding'])

    def test_negative_reference_weight_remains_visible(self):
        self.points['holdingPercent']['value'][1] = '-0.10000'
        result = compare(self.provider, self.issuer)
        self.assertEqual(1, result['negative_issuer_weight_rows'])


if __name__ == '__main__':
    unittest.main()
