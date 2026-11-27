# ESILV MarketPulse - HANEteam (G01)

![Course: MESIFI472326](https://img.shields.io/badge/course-MESIFI472326-1f6feb.svg)
![ESILV A4](https://img.shields.io/badge/ESILV-A4-111827.svg)
![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg)

Team repository for the ESILV A4 module **Python, Git, Linux** (MESIFI472326).

Team members: see [TEAM.md](TEAM.md).

## What is MarketPulse?

MarketPulse is a Python application that compares one financial instrument with its market benchmark over the same period and frequency.

It answers:

> Is the instrument outperforming or underperforming its benchmark?

## Market

```text
Instrument : AAPL - Apple Inc.
Benchmark  : S&P 500 (SP500)
Lookback   : 1 month
Interval   : Daily
```

Calculated values: period return, base 100, relative performance (instrument minus benchmark, in percentage points).

## Provider

Final provider:

```text
Bloomberg stage - APPROVED_SAMPLE
```

Source: `data/sample/bloomberg_reference_sample.json` (instructor-approved teaching sample).

Live Bloomberg connectivity was not demonstrated. These values are teaching data, not live Bloomberg output.

The Yahoo Finance provider (`src/providers/yahoo_provider.py`) is still available: set `PROVIDER = "yahoo"` in `src/main.py`.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run

Run from the repository root.

Terminal:

```bash
python src/main.py
```

Dashboard:

```bash
python src/dashboard.py
```

Then open http://127.0.0.1:8050 (in Codespaces, open the forwarded port 8050).

## Environment constraints

- Commands must be run from the repository root (data paths are relative to it).
- The final provider (APPROVED_SAMPLE) does not need internet access or a Bloomberg terminal.
- The Yahoo Finance provider needs internet access; its values depend on the retrieval date.
- Live Bloomberg requires the instructor-approved Bloomberg environment.

## Architecture

```text
src/
├── main.py                    build_market_snapshot() + terminal output
├── analytics.py               alignment, period return, base 100, relative performance
├── dashboard.py               Dash presentation of the snapshot
└── providers/
    ├── __init__.py
    ├── yahoo_provider.py
    └── bloomberg_provider.py
```

```text
provider -> canonical rows -> analytics.py -> build_market_snapshot() -> terminal / Dash
```

Bloomberg mapping: [docs/BLOOMBERG_FIELD_MAPPING.md](docs/BLOOMBERG_FIELD_MAPPING.md).

## Evidence

Checkpoint evidence is stored under:

```text
evidence/checkpoint-a/<github-username>/
evidence/checkpoint-b/<github-username>/
evidence/checkpoint-c/<github-username>/
```

See [evidence/README.md](evidence/README.md).

## Security

No password, API key, token or Bloomberg credential is committed.
