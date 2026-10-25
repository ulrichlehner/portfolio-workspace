# Independent fund-data verification

This is workspace verification tooling, not a PP runtime provider. Use independent
public samples only. Do not upload a portfolio or send quantities, balances or
credentials. Provider and issuer payloads and full comparison reports stay in
ignored `scratch/` storage, never in fixtures or commits. Only synthetic tests
ship with the tooling.

## Source discovery and comparison

The convenient iShares CSV lacks constituent ISINs. The product page's public
`holdings` component supplies parallel arrays for ISIN, name, asset class, weight,
market value and notional value, plus an effective date. Its request contract is
used by the page's `ProductPageAjaxUtils` script. Follow the current page rather
than assuming the endpoint is stable forever.

Observed endpoint on 2026-10-25:

```text
https://www.blackrock.com/varnish-api/uk-retail01-product-data/product-data/api/v2/get-product-data
```

Observed query fields: `appSubType=ISHARES`, `appType=PRODUCT_PAGE`,
`component=holdings`, `locale=en_GB`, `portfolioId=<public-product-id>`,
`targetSite=ishares-uk`, `userType=individual`, `excludeContent=true`,
`includeConfig=true`, `asOfDate=YYYYMMDD`.

Check the returned `asOfDate.value`, not just the requested date. The API's raw
weights have more precision than the rounded CSV display. A provider update
timestamp does not establish a holdings date. Similar names do not establish
company identity. Do not infer a row's value currency from a different endpoint.

## Run offline in Docker

After saving independent public source files locally:

```sh
docker run --rm --network none \
  -v "$PWD/scripts":/tools:ro -v "$PWD/scratch":/data:ro -w /tools \
  portfolio-dev python3 compare_fund_holdings.py \
  --provider /data/public-provider.json --issuer /data/public-issuer.json \
  > scratch/public-comparison.json
```

The script reads local inputs only. It compares unique exact ISIN pairs, checks
parallel-array lengths and finite decimal values, preserves duplicate groups as
unresolved and reports every unmatched row. Exact-name candidates for rows without
ISIN are diagnostics only and never count as verified identities. Zero-market-value
rows with positive notional remain visible. Currency-scale ratios are reported
without asserting currency equivalence. It never certifies complete economic
exposure merely because identified weights agree.

Ordinary synthetic regression tests run with:

```sh
scripts/dev.sh test-tools
```

## Dated acceptance evidence

The complete 22 Oct 2026 issuer lists were compared against the two independently
chosen public Eulerpool samples on 25 Oct. All 1251 identified World rows and all
101 identified NASDAQ rows matched issuer ISINs; every paired weight agreed within
the combined raw rounding tolerance of 0.000005005 percentage points. No duplicate
ISIN groups occurred. The issuer supplied asset classifications for all of them.

The provider omitted four World and one NASDAQ futures rows with zero market value
but positive notional. The World issuer also reported a zero-balance cash row.
Remaining provider rows without ISIN have exact cash/collateral name candidates,
not verified identifier mappings. Source values and profile AUM cannot be compared
naively across currencies, share-class/fund scope and dates.

Detailed evidence and remaining acceptance criteria are in
`openspec/changes/automatic-portfolio-xray/provider-gates.md`. Historical agreement
does not validate every future response, a company graph or the omitted economic
derivative exposure. The PP application does not yet retrieve or apply this issuer
evidence, so a successful offline comparison is not claimed as runtime integration.
