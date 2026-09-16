import json
from pathlib import Path

from src.models import AirfareObservation
from src.normalizer import validate_observation
from src.deduplicator import deduplicate_observations
from src.index_engine import calculate_daily_index, calculate_route_indices


from src.routes import ROUTES, BOOKING_WINDOWS

def make_observation(**overrides):
    data = {
        "observation_id": "TEST-001",
        "source": "test",
        "collected_at": "2026-09-13T10:00:00",
        "origin": "DEL",
        "destination": "BOM",
        "carrier": "TEST",
        "travel_date": "2026-09-20",
        "booking_window": 7,
        "total_fare": 5000.0,
        "base_fare": 3750.0,
        "taxes": 1000.0,
        "fees": 250.0,
        "fare_class": "economy",
        "stops": 0,
        "duration_minutes": 135,
        "availability_status": "available",
    }

    data.update(overrides)
    return AirfareObservation(**data)


def test_observation_model_accepts_valid_data():
    observation = make_observation()

    assert observation.origin == "DEL"
    assert observation.destination == "BOM"
    assert observation.total_fare == 5000.0


def test_normalizer_accepts_valid_observation():
    observation = make_observation()

    errors = validate_observation(observation)

    assert errors == []


def test_normalizer_rejects_negative_fare():
    observation = make_observation(total_fare=-100)

    errors = validate_observation(observation)

    assert len(errors) > 0


def test_normalizer_rejects_same_origin_destination():
    observation = make_observation(destination="DEL")

    errors = validate_observation(observation)

    assert len(errors) > 0


def test_deduplicator_removes_duplicate_observations():
    observations = [
        make_observation(),
        make_observation(),
        make_observation(
            observation_id="TEST-002",
            total_fare=5200.0,
            base_fare=3900.0,
            taxes=1040.0,
            fees=260.0,
        ),
    ]

    result = deduplicate_observations(observations)

    assert len(result) == 2


def test_route_index_ignores_sold_out_observations():
    observations = [
        make_observation(
            observation_id="AVAILABLE",
            total_fare=5000.0,
        ).model_dump(),
        make_observation(
            observation_id="SOLD-OUT",
            total_fare=9999.0,
            availability_status="sold_out",
        ).model_dump(),
    ]

    results = calculate_route_indices(observations)

    assert len(results) == 1
    assert results[0]["observations"] == 1
    assert results[0]["base_price"] == 5000.0


def test_daily_index_returns_expected_structure():
    observations = [
        make_observation(
            observation_id="DAY-1",
            collected_at="2026-09-13T10:00:00",
            total_fare=5000.0,
        ).model_dump(mode="json"),
        make_observation(
            observation_id="DAY-2",
            collected_at="2026-09-14T10:00:00",
            total_fare=5500.0,
        ).model_dump(mode="json"),
    ]

    results = calculate_daily_index(observations)

    assert len(results) == 2
    assert results[0]["date"] == "2026-09-13"
    assert results[0]["index"] == 100.0
    assert results[1]["index"] > 100.0


def test_generated_collection_file_exists():
    path = Path("data/raw/collected_airfares.json")

    assert path.exists()

    with path.open() as f:
        observations = json.load(f)

    assert len(observations) == 35


def test_weighted_daily_index_uses_all_strata():
    from src.index_engine import calculate_weighted_daily_index

    observations = [
        {
            "collected_at": "2026-08-15T10:00:00",
            "origin": route["origin"],
            "destination": route["destination"],
            "booking_window": window,
            "total_fare": 1000,
            "availability_status": "available",
        }
        for route in ROUTES
        for window in BOOKING_WINDOWS
    ]

    observations += [
        {
            "collected_at": "2026-08-16T10:00:00",
            "origin": route["origin"],
            "destination": route["destination"],
            "booking_window": window,
            "total_fare": 1100,
            "availability_status": "available",
        }
        for route in ROUTES
        for window in BOOKING_WINDOWS
    ]

    results = calculate_weighted_daily_index(observations)

    assert len(results) == 2
    assert results[0]["index"] == 100.0
    assert results[1]["index"] == 110.0
    assert results[1]["route_window_groups"] == 35
    assert results[1]["weight_coverage"] == 1.0
