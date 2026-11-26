# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
- Instructor reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` (not present in the team repository)
- Live connectivity: **not demonstrated**

The sample declares `"access_mode": "approved_sample"` and `"is_live_bloomberg_output": false`.
Its values are illustrative teaching values reused from `data/sample/prices.csv`,
not certified Bloomberg historical observations.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

Provider identifiers by stage:

| Canonical ticker | CSV | Yahoo | Bloomberg |
|---|---|---|---|
| AAPL | AAPL | AAPL | AAPL US Equity |
| SP500 | SP500 | ^GSPC | SPX Index |

The canonical tickers `AAPL` and `SP500` are the only identifiers that reach `analytics.py`.

## Inspected input

| Series | `provider_identifier` | `canonical_ticker` | Observations | First date | Last date |
|---|---|---|---|---|---|
| Instrument | AAPL US Equity | AAPL | 21 | 2026-09-01 | 2026-09-30 |
| Benchmark | SPX Index | SP500 | 21 | 2026-09-01 | 2026-09-30 |

Structure: one top-level object with a `series` list. Each series holds
`role`, `canonical_ticker`, `provider_identifier` and an `observations` list.

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | teaching wrapper key, ISO string `YYYY-MM-DD` |
| ticker | application mapping from `canonical_ticker` | `AAPL` or `SP500`, never the Bloomberg identifier |
| open | `open_value` | teaching wrapper key, convert to `float` |
| high | `high_value` | teaching wrapper key, convert to `float` |
| low | `low_value` | teaching wrapper key, convert to `float` |
| close | `close_value` | teaching wrapper key, convert to `float` |
| volume | `volume_value` | teaching wrapper key, convert to `int` |

**Teaching wrapper key ≠ Bloomberg LIVE field mnemonic.**
No LIVE Bloomberg field name was observed, so none is documented here.

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity → canonical ticker AAPL
- Benchmark identifier: SPX Index → canonical ticker SP500
- Date representation: ISO string `YYYY-MM-DD` in `observation_date`
- Input structure: `series[]` → `observations[]`
- Missing fields: none, no null value in either series
- Special normalization notes:
  - some prices are stored as JSON integers (for example `6742`): always convert with `float()`;
  - SPX Index volume is `0` for every observation, because an index is not traded directly;
  - the provider must output `ticker` from `canonical_ticker`, not from `provider_identifier`.
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json` (42 rows, 21 per ticker)