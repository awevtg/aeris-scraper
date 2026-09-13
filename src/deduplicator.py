from src.models import AirfareObservation


def duplicate_key(observation: AirfareObservation):
    """
    Build a stable key for detecting identical airfare observations.
    """
    return (
        observation.source,
        observation.carrier,
        observation.origin,
        observation.destination,
        observation.travel_date,
        observation.booking_window,
        observation.fare_class,
        observation.stops,
        observation.duration_minutes,
        round(observation.total_fare, 2),
    )


def deduplicate_observations(observations):
    """
    Keep the first occurrence of each identical observation.
    """
    unique = []
    seen = set()

    for observation in observations:
        key = duplicate_key(observation)

        if key in seen:
            continue

        seen.add(key)
        unique.append(observation)

    return unique
