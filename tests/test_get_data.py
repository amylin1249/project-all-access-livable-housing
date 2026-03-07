from datetime import datetime
from src.get_data import get_evictions_data


def test_api_fetch():
    results = get_evictions_data()
    assert isinstance(results, list)

def test_api_conversion():
    results = get_evictions_data()
    sample = results[0]
    assert len(sample) == 4

    assert isinstance(sample["id"], int)
    assert isinstance(sample["lat"], float)
    assert isinstance(sample["lon"], float)
    assert isinstance(sample["year_mon"], str)


def test_api_year_in_range():
    results = get_evictions_data()
    for date in results:
        year = int(date["year_mon"][:4])
        assert 2020 <= year <= 2024

def test_api_coordinates_valid():
    results = get_evictions_data()
    for record in results:
        # lat and lon of SF
        assert 37.0 <= record["lat"] <= 38.5
        assert -123.0 <= record["lon"] <= -122.0