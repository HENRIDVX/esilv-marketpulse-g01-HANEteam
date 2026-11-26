
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

from providers.bloomberg_provider import (
    fetch_bloomberg_prices,
    ACCESS_MODE,
)

DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(
        DATA_DIR / "instruments.json",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def load_prices():
    with open(
        DATA_DIR / "prices.csv",
        encoding="utf-8",
    ) as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [
        row for row in prices
        if row["ticker"] == ticker
    ]


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


def build_market_snapshot():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    # Bloomberg data acquisition
    instrument_prices = fetch_bloomberg_prices(
        instrument["ticker"]
    )

    benchmark_prices = fetch_bloomberg_prices(
        benchmark["ticker"]
    )

    # Align common dates
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument or not aligned_benchmark:
        raise ValueError("No common dates found")

    # Period returns
    instrument_return = calculate_period_return(
        aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    # Relative performance
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    # Base 100
    instrument_base_100 = calculate_base_100(
        aligned_instrument
    )

    benchmark_base_100 = calculate_base_100(
        aligned_benchmark
    )

    # Shared application snapshot
    return {
        "provider": f"Bloomberg stage - {ACCESS_MODE}",
        "access_mode": ACCESS_MODE,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
        "instrument_prices": aligned_instrument,
        "benchmark_prices": aligned_benchmark,
    }


def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    instrument_prices = snapshot["instrument_prices"]
    benchmark_prices = snapshot["benchmark_prices"]

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]

    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")
    print()

    print("Provider")
    print(snapshot["provider"])
    print()

    print("Access mode")
    print(snapshot["access_mode"])
    print()

    print("Market configuration")
    print(f"Period: {snapshot['lookback']}")
    print(f"Interval: {snapshot['interval']}")
    print()

    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(
        f"Last price: {instrument_latest['close']:.2f}"
        f" {instrument['currency']}"
    )
    print(
        f"Period return: "
        f"{snapshot['instrument_return']:.2f}%"
    )
    print()

    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Last level: {benchmark_latest['close']:.2f}")
    print(
        f"Period return: "
        f"{snapshot['benchmark_return']:.2f}%"
    )
    print()

    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']}: "
        f"{snapshot['relative_performance']:+.2f}"
        f" percentage points"
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
    print(f"{instrument['ticker']}: {len(instrument_prices)}")
    print(f"{benchmark['ticker']}: {len(benchmark_prices)}")

    print(
        f"First common date: "
        f"{instrument_prices[0]['date']}"
    )

    print(
        f"Last common date: "
        f"{instrument_prices[-1]['date']}"
    )
    print()

    print("Bloomberg sample market data")
    print(instrument_latest)
    print(benchmark_latest)


if __name__ == "__main__":
    main()