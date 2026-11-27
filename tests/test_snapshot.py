from main import build_market_snapshot


def test_snapshot_bloomberg_sample():
    snapshot = build_market_snapshot()
    assert snapshot["access_mode"] == "APPROVED_SAMPLE"
    assert snapshot["lookback"] == "1 month"
    assert snapshot["interval"] == "Daily"
    assert len(snapshot["instrument_prices"]) == len(snapshot["benchmark_prices"])
    assert round(snapshot["instrument_return"], 2) == 6.48
    assert round(snapshot["benchmark_return"], 2) == 2.15
    assert round(snapshot["relative_performance"], 2) == 4.33
