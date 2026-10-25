#!/usr/bin/env python3
"""Offline issuer comparison; inputs and reports belong in private scratch storage.

This is verification tooling, not a runtime adapter or a certificate of complete
economic exposure. No requests, credential access, fuzzy matching or persistence
of provider data are performed by this module.
"""

import argparse
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
from statistics import median


def number(value):
    if isinstance(value, bool) or value is None:
        raise ValueError('Missing or invalid numeric value')
    try:
        result = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError('Invalid numeric value') from error
    if not result.is_finite():
        raise ValueError('Nonfinite numeric value')
    return result


def identifier(value):
    return value.strip() if isinstance(value, str) and value.strip() not in ('', '-', '--') else None


def provider_rows(data):
    if not isinstance(data, list) or not data:
        raise ValueError('Expected nonempty provider holdings array')
    return [dict(isin=identifier(row.get('isin')), name=row.get('name', ''),
                 weight=number(row.get('percent')), value=number(row.get('value')),
                 asset_class=row.get('assetType'), updated_at=row.get('updated_at')) for row in data]


def issuer_rows(data):
    points = data['componentsByNameMap']['holdings']['containersByNameMap']['all']['dataPointsByNameMap']
    date = str(points['asOfDate']['value'])
    datetime.strptime(date, '%Y%m%d')
    names = points['issueName']['value']
    if not isinstance(names, list) or not names:
        raise ValueError('Expected nonempty issuer holdings arrays')
    fields = {'isin': 'isin', 'name': 'issueName', 'weight': 'holdingPercent',
              'value': 'marketValue', 'notional': 'notionalValue', 'asset_class': 'assetClass'}
    arrays = {target: points[source]['value'] for target, source in fields.items()}
    if any(not isinstance(values, list) or len(values) != len(names) for values in arrays.values()):
        raise ValueError('Issuer parallel arrays have inconsistent lengths')
    rows = []
    for index in range(len(names)):
        row = {key: values[index] for key, values in arrays.items()}
        row['isin'] = identifier(row['isin'])
        for key in ('weight', 'value', 'notional'):
            row[key] = number(row[key])
        rows.append(row)
    return date, rows


def groups(rows, key):
    result = defaultdict(list)
    for index, row in enumerate(rows):
        value = row[key]
        if value:
            result[value].append(index)
    return result


def decimal_summary(values):
    return dict(minimum=min(values), median=median(values), maximum=max(values)) if values else None


def compare(provider, issuer):
    source = provider_rows(provider)
    date, reference = issuer_rows(issuer)
    left, right = groups(source, 'isin'), groups(reference, 'isin')
    matched = []
    for isin in sorted(left.keys() & right.keys()):
        # Preserve multiplicity. Duplicate groups need a separate semantics
        # review, not a zip, deduplication or automatic weight aggregation.
        if len(left[isin]) == len(right[isin]) == 1:
            matched.append((left[isin][0], right[isin][0]))
    used_left = {a for a, _ in matched}
    used_right = {b for _, b in matched}
    differences = [abs(source[a]['weight'] - reference[b]['weight']) for a, b in matched]
    nonzero = [row['weight'] for row in reference if row['weight']]
    # Raw issuer weights have more precision than the visible two-decimal CSV.
    quantum = Decimal(1).scaleb(min(value.as_tuple().exponent for value in nonzero))
    source_quantum = Decimal(1).scaleb(min(row['weight'].as_tuple().exponent for row in source))
    tolerance = (quantum + source_quantum) / 2
    scale = [reference[b]['value'] / source[a]['value'] for a, b in matched
             if source[a]['value'] > 0 and reference[b]['value'] > 0]
    missing_source = [row for i, row in enumerate(source) if i not in used_left]
    missing_reference = [row for i, row in enumerate(reference) if i not in used_right]
    # Exact-name candidates explain identifierless rows only. They are never
    # counted as ISIN-verified, nor returned as runtime classification evidence.
    names_left = groups(missing_source, 'name')
    names_right = groups(missing_reference, 'name')
    name_candidates = []
    for name in sorted(names_left.keys() & names_right.keys()):
        if len(names_left[name]) == len(names_right[name]) == 1:
            a = missing_source[names_left[name][0]]
            b = missing_reference[names_right[name][0]]
            if a['isin'] is None and b['isin'] is None:
                name_candidates.append(dict(name=name, issuer_class=b['asset_class'],
                                            difference_pp=abs(a['weight'] - b['weight'])))
    classes = {}
    for asset_class in sorted({row['asset_class'] for row in reference}):
        rows = [row for row in reference if row['asset_class'] == asset_class]
        classes[asset_class] = dict(rows=len(rows), weight_sum=sum(row['weight'] for row in rows),
                                    market_value=sum(row['value'] for row in rows),
                                    notional_value=sum(row['notional'] for row in rows))
    return dict(
        issuer_effective_date=date,
        provider_update_dates=sorted({row['updated_at'] for row in source if row['updated_at']}),
        provider_holdings_effective_date=None,
        provider_rows=len(source), issuer_rows=len(reference),
        provider_weight_sum=sum(row['weight'] for row in source),
        issuer_weight_sum=sum(row['weight'] for row in reference),
        provider_market_value_sum=sum(row['value'] for row in source),
        issuer_market_value_sum=sum(row['value'] for row in reference),
        isin_matched_rows=len(matched),
        isin_matched_provider_weight=sum(source[a]['weight'] for a, _ in matched),
        isin_matched_issuer_weight=sum(reference[b]['weight'] for _, b in matched),
        duplicate_provider_isins={key: len(value) for key, value in left.items() if len(value) > 1},
        duplicate_issuer_isins={key: len(value) for key, value in right.items() if len(value) > 1},
        provider_rows_without_isin=sum(row['isin'] is None for row in source),
        issuer_rows_without_isin=sum(row['isin'] is None for row in reference),
        weight_difference_pp=decimal_summary(differences),
        weight_difference_absolute_sum_pp=sum(differences),
        issuer_raw_weight_quantum_pp=quantum, combined_rounding_tolerance_pp=tolerance,
        isin_matches_within_rounding=sum(value <= tolerance for value in differences),
        issuer_to_provider_market_value_ratio=decimal_summary(scale),
        # No currency equivalence is inferred: the API rows omit value currency.
        issuer_reporting_currency=issuer.get('currencyCode'), provider_row_value_currency=None,
        unmatched_provider_rows=missing_source, unmatched_issuer_rows=missing_reference,
        identifierless_name_candidates=name_candidates, issuer_asset_classes=classes,
        zero_value_positive_notional_rows=[row for row in reference if row['value'] == 0 and row['notional'] > 0],
        negative_issuer_weight_rows=sum(row['weight'] < 0 for row in reference),
        validated_complete_economic_exposure=False,
        limitations=['Provider effective date is not inferred from its update time.',
                     'Security ISIN matching does not establish a corporate identity graph.',
                     'Identifierless name candidates are diagnostics, not verified identities.',
                     'Market-value weights do not by themselves represent derivative economic exposure.',
                     'Agreement with this issuer vintage does not certify future provider snapshots.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider', required=True, type=Path)
    parser.add_argument('--issuer', required=True, type=Path)
    args = parser.parse_args()
    load = lambda path: json.loads(path.read_text(encoding='utf-8'), parse_float=Decimal)
    print(json.dumps(compare(load(args.provider), load(args.issuer)), default=str, indent=2))


if __name__ == '__main__':
    main()
