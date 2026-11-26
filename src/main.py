
from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

from providers.yahoo_provider import (
    fetch_yahoo_prices,
    YAHOO_SYMBOLS,
)

DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def main():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    # Retrieve Yahoo Finance data
    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[instrument["ticker"]],
        canonical_ticker=instrument["ticker"],
        period="1mo",
        interval="1d",
    )

    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[benchmark["ticker"]],
        canonical_ticker=benchmark["ticker"],
        period="1mo",
        interval="1d",
    )

    # Align common dates
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument or not aligned_benchmark:
        raise ValueError("No common dates found")

    # Calculate period returns
    instrument_return = calculate_period_return(
        aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    # Calculate relative performance
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    # Calculate base 100
    instrument_base_100 = calculate_base_100(
        aligned_instrument
    )

    benchmark_base_100 = calculate_base_100(
        aligned_benchmark
    )

    instrument_latest = aligned_instrument[-1]
    benchmark_latest = aligned_benchmark[-1]

    # Display results
    print("=== MarketPulse ===")
    print()

    print("Provider")
    print("Yahoo Finance via yfinance")
    print()

    print("Market configuration")
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()

    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Last price: {instrument_latest['close']:.2f} {instrument['currency']}")
    print(f"Period return: {instrument_return:.2f}%")
    print()

    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Last level: {benchmark_latest['close']:.2f}")
    print(f"Period return: {benchmark_return:.2f}%")
    print()

    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']}: "
        f"{relative_performance:+.2f} percentage points"
    )
    print()

    print("Base 100")
    print(
        f"{instrument['ticker']}: "
        f"{instrument_base_100[0]['value']:.2f} -> "
        f"{instrument_base_100[-1]['value']:.2f}"
    )

    print(
        f"{benchmark['ticker']}: "
        f"{benchmark_base_100[0]['value']:.2f} -> "
        f"{benchmark_base_100[-1]['value']:.2f}"
    )
    print()

    print("Observations")
    print(f"{instrument['ticker']}: {len(aligned_instrument)}")
    print(f"{benchmark['ticker']}: {len(aligned_benchmark)}")
    print(f"First common date: {aligned_instrument[0]['date']}")
    print(f"Last common date: {aligned_instrument[-1]['date']}")
    print()

    print("Yahoo market data")
    print(instrument_latest)
    print(benchmark_latest)


if __name__ == "__main__":
    main()
