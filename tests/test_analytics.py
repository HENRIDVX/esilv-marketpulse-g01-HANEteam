from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)


def row(date, close, ticker="AAPL"):
    return {"date": date, "ticker": ticker, "close": close}


def test_period_return():
    prices = [row("2026-09-01", 100.0), row("2026-09-30", 110.0)]
    assert round(calculate_period_return(prices), 2) == 10.0


def test_base_100_starts_at_100():
    prices = [row("2026-09-01", 250.0), row("2026-09-02", 275.0)]
    result = calculate_base_100(prices)
    assert result[0]["value"] == 100.0
    assert round(result[-1]["value"], 2) == 110.0


def test_relative_performance():
    assert round(calculate_relative_performance(6.48, 2.15), 2) == 5.00


def test_align_series_keeps_common_dates():
    instrument = [row("2026-09-01", 1.0), row("2026-09-02", 2.0)]
    benchmark = [row("2026-09-02", 3.0, "SP500"), row("2026-09-03", 4.0, "SP500")]
    aligned_instrument, aligned_benchmark = align_series(instrument, benchmark)
    assert [r["date"] for r in aligned_instrument] == ["2026-09-02"]
    assert [r["date"] for r in aligned_benchmark] == ["2026-09-02"]
