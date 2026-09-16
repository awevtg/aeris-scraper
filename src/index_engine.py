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

        # Only available fares enter the price index.
        # Sold-out and cancelled observations are retained in the
        # raw dataset but excluded from price measurement.
        if obs.get("availability_status", "available") != "available":
            continue

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


def calculate_weighted_daily_index(observations):
    """
    Calculate the AERIS daily index using explicit route ×
    booking-window weights.

    Current MVP weights are equal-weight fallbacks from src.weights.
    They can later be replaced with validated DGCA traffic weights
    and empirical booking-window shares.

    Each route × booking-window stratum is first indexed against
    its own first available observation. The national daily index
    is then the weighted geometric aggregation of those strata.
    """
    from src.weights import build_stratum_weights

    strata = build_stratum_weights()

    stratum_lookup = {
        (
            item["origin"],
            item["destination"],
            item["booking_window"],
        ): item["combined_weight"]
        for item in strata
    }

    groups = defaultdict(list)

    for obs in observations:
        if obs.get("availability_status", "available") != "available":
            continue

        fare = obs.get("total_fare", 0)

        if fare <= 0:
            continue

        collection_date = obs["collected_at"][:10]
        key = (
            obs["origin"],
            obs["destination"],
            obs["booking_window"],
        )

        groups[key].append(
            {
                "date": collection_date,
                "fare": fare,
            }
        )

    base_prices = {}

    for key, items in groups.items():
        items = sorted(items, key=lambda x: x["date"])

        for item in items:
            if item["fare"] > 0:
                base_prices[key] = item["fare"]
                break

    daily_strata = defaultdict(list)

    for key, items in groups.items():
        base_price = base_prices.get(key)
        weight = stratum_lookup.get(key)

        if not base_price or not weight:
            continue

        for item in items:
            if item["fare"] <= 0:
                continue

            relative_price = item["fare"] / base_price

            daily_strata[item["date"]].append(
                {
                    "relative_price": relative_price,
                    "weight": weight,
                }
            )

    daily_results = []

    for collection_date in sorted(daily_strata.keys()):
        items = daily_strata[collection_date]

        weighted_log_sum = 0.0
        total_weight = 0.0

        for item in items:
            weighted_log_sum += (
                item["weight"]
                * math.log(item["relative_price"])
            )
            total_weight += item["weight"]

        if total_weight <= 0:
            continue

        index = math.exp(weighted_log_sum / total_weight) * 100

        daily_results.append(
            {
                "date": collection_date,
                "index": round(index, 4),
                "route_window_groups": len(items),
                "weight_coverage": round(total_weight, 6),
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
            if item["total_fare"] > 0 and item.get("availability_status") == "available"
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
