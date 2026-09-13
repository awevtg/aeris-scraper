import json
import math
from collections import defaultdict
from pathlib import Path


def load_observations(path: str):
    with open(path, "r") as f:
        return json.load(f)


def geometric_mean(values):
    if not values:
        return None

    log_values = [math.log(v) for v in values if v > 0]

    if not log_values:
        return None

    return math.exp(sum(log_values) / len(log_values))


def calculate_daily_index(observations):
    """
    Calculate a daily route × booking-window price index.

    Each route/window stratum is indexed relative to its
    first observed price, then aggregated using a geometric mean.
    """

    # Group observations by route, booking window and collection date
    groups = defaultdict(list)

    for obs in observations:
        collection_date = obs["collected_at"][:10]

        key = (
            obs["origin"],
            obs["destination"],
            obs["booking_window"],
        )

        groups[key].append(
            {
                "date": collection_date,
                "fare": obs["total_fare"],
            }
        )

    # Determine base fare for each route × window
    base_prices = {}

    for key, items in groups.items():
        items = sorted(items, key=lambda x: x["date"])

        for item in items:
            if item["fare"] > 0:
                base_prices[key] = item["fare"]
                break

    # Calculate daily route/window indices
    daily_groups = defaultdict(list)

    for key, items in groups.items():
        base_price = base_prices.get(key)

        if not base_price:
            continue

        for item in items:
            if item["fare"] <= 0:
                continue

            price_relative = item["fare"] / base_price

            daily_groups[item["date"]].append(
                price_relative
            )

    # Aggregate route/window relatives into national index
    daily_results = []

    for collection_date in sorted(daily_groups.keys()):
        relatives = daily_groups[collection_date]

        index = geometric_mean(relatives) * 100

        daily_results.append(
            {
                "date": collection_date,
                "index": round(index, 4),
                "route_window_groups": len(relatives),
            }
        )

    return daily_results


def calculate_route_indices(observations):
    """
    Calculate route-level indices relative to the first
    observed fare for each route.
    """

    groups = defaultdict(list)

    for obs in observations:
        key = (
            obs["origin"],
            obs["destination"],
        )

        groups[key].append(obs)

    results = []

    for (origin, destination), items in groups.items():

        items = sorted(
            items,
            key=lambda x: x["collected_at"]
        )

        valid_items = [
            item
            for item in items
            if item["total_fare"] > 0
        ]

        if not valid_items:
            continue

        base_price = valid_items[0]["total_fare"]

        relatives = [
            item["total_fare"] / base_price
            for item in valid_items
        ]

        index = geometric_mean(relatives) * 100

        results.append(
            {
                "origin": origin,
                "destination": destination,
                "index": round(index, 4),
                "base_price": base_price,
                "observations": len(valid_items),
            }
        )

    return results


if __name__ == "__main__":

    input_path = Path(
        "data/raw/backtest_airfares.json"
    )

    observations = load_observations(
        str(input_path)
    )

    daily_results = calculate_daily_index(
        observations
    )

    route_results = calculate_route_indices(
        observations
    )

    print(
        f"Daily index points: {len(daily_results)}"
    )

    print(
        f"Route results: {len(route_results)}"
    )

    print("\nDaily Airfare Price Index:")

    for result in daily_results:
        print(result)

    print("\nRoute-level indices:")

    for result in route_results:
        print(result)
