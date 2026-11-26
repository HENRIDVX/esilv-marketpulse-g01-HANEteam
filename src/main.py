from pathlib import Path
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
YAHOO_PERIOD = "1mo"
YAHOO_INTERVAL = "1d"
PROVIDER_LABEL = "Yahoo Finance via yfinance"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def fetch_series(asset):
    ticker = asset["ticker"]
    return fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[ticker],
        canonical_ticker=ticker,
        period=YAHOO_PERIOD,
        interval=YAHOO_INTERVAL,
    )


def display_market_summary(asset, prices, period_return, show_currency=True):
    currency = f" {asset['currency']}" if show_currency else ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Yahoo symbol  : {YAHOO_SYMBOLS[asset['ticker']]}")
    print(f"Observations  : {len(prices)}")
    print(f"First date    : {prices[0]['date']}")
    print(f"Last date     : {prices[-1]['date']}")
    print(f"First close   : {prices[0]['close']:.2f}{currency}")
    print(f"Last close    : {prices[-1]['close']:.2f}{currency}")
    print(f"Period return : {period_return:.2f}%")


def main():
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_series(instrument)
    benchmark_prices = fetch_series(benchmark)

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument:
        raise ValueError("No common dates between instrument and benchmark")

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(PROVIDER_LABEL)
    print()
    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {LOOKBACK_LABEL}")
    print(f"Interval   : {INTERVAL_LABEL}")
    print()
    print("Instrument")
    display_market_summary(instrument, aligned_instrument, instrument_return)
    print()
    print("Benchmark")
    display_market_summary(
        benchmark,
        aligned_benchmark,
        benchmark_return,
        show_currency=False,
    )
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} percentage points"
    )
    print()
    print("Base 100")
    print(
        f"{instrument['ticker']:<5} : "
        f"{instrument_base_100[0]['value']:.2f} -> "
        f"{instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<5} : "
        f"{benchmark_base_100[0]['value']:.2f} -> "
        f"{benchmark_base_100[-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()