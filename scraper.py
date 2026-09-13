import json
from datetime import date, timedelta
from pathlib import Path

from src.collectors.register_sources import register_default_sources
from src.normalizer import validate_observation
from src.deduplicator import deduplicate_observations
from src.routes import ROUTES, BOOKING_WINDOWS


OUTPUT_PATH = Path("data/raw/collected_airfares.json")


def run_collection():
    source_registry = register_default_sources()
    adapter = source_registry.get("sample_source")

    collected = []
    invalid = []
    today = date.today()

    for route in ROUTES:
        for booking_window in BOOKING_WINDOWS:
            travel_date = today + timedelta(days=booking_window)

            observations = adapter.collect(
                origin=route["origin"],
                destination=route["destination"],
                travel_date=travel_date.isoformat(),
                booking_window=booking_window,
            )

            for observation in observations:
                errors = validate_observation(observation)

                if errors:
                    invalid.append({
                        "observation": observation.model_dump(mode="json"),
                        "errors": errors,
                    })
                else:
                    collected.append(observation.model_dump(mode="json"))

    collected_observations = [
        __import__("src.models", fromlist=["AirfareObservation"])
        .AirfareObservation.model_validate(item)
        for item in collected
    ]

    before_deduplication = len(collected_observations)
    collected_observations = deduplicate_observations(
        collected_observations
    )
    duplicates_removed = (
        before_deduplication - len(collected_observations)
    )

    collected = [
        observation.model_dump(mode="json")
        for observation in collected_observations
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w") as f:
        json.dump(collected, f, indent=2)

    error_path = Path("data/processed/collection_errors.json")
    error_path.parent.mkdir(parents=True, exist_ok=True)

    with error_path.open("w") as f:
        json.dump(invalid, f, indent=2)

    print(f"Collection complete: {len(collected)} valid observations")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Invalid observations: {len(invalid)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"Errors saved to: {error_path}")


if __name__ == "__main__":
    run_collection()
