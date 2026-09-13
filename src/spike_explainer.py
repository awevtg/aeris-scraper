import json
from pathlib import Path
from src.index_engine import load_observations, calculate_daily_index


INPUT = Path("data/raw/backtest_airfares.json")
ANOMALIES = Path("data/processed/anomalies.json")
OUTPUT = Path("data/processed/spike_explanations.json")


def get_route_movements(observations, target_date):
    """
    Find route-level fare movements on a particular date.
    """

    previous = {}
    current = {}

    for obs in observations:
        key = (
            obs["origin"],
            obs["destination"],
            obs["booking_window"],
        )

        date = obs["collected_at"][:10]

        if date < target_date:
            previous[key] = obs["total_fare"]

        elif date == target_date:
            current[key] = obs["total_fare"]

    movements = []

    for key, current_fare in current.items():

        previous_fare = previous.get(key)

        if previous_fare is None or previous_fare <= 0:
            continue

        change_pct = (
            (current_fare - previous_fare)
            / previous_fare
        ) * 100

        movements.append({
            "origin": key[0],
            "destination": key[1],
            "booking_window": key[2],
            "previous_fare": round(previous_fare, 2),
            "current_fare": round(current_fare, 2),
            "change_pct": round(change_pct, 2),
        })

    return sorted(
        movements,
        key=lambda x: x["change_pct"],
        reverse=True,
    )


def severity(index_change):

    if index_change >= 10:
        return "HIGH"

    if index_change >= 5:
        return "MEDIUM"

    return "LOW"


def main():

    with open(ANOMALIES, "r") as f:
        anomalies = json.load(f)

    observations = load_observations(str(INPUT))

    daily_index = calculate_daily_index(
        observations
    )

    explanations = []

    for i, item in enumerate(daily_index):

        if i == 0:
            continue

        previous_index = daily_index[i - 1]["index"]
        current_index = item["index"]

        change_pct = (
            (current_index - previous_index)
            / previous_index
        ) * 100

        # Only explain meaningful upward movements.
        if change_pct < 3:
            continue

        route_movements = get_route_movements(
            observations,
            item["date"],
        )

        top_routes = route_movements[:5]

        explanations.append({
            "date": item["date"],
            "index": current_index,
            "previous_index": previous_index,
            "index_change_pct": round(change_pct, 2),
            "severity": severity(change_pct),
            "top_affected_routes": top_routes,
        })

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(OUTPUT, "w") as f:
        json.dump(
            explanations,
            f,
            indent=2,
        )

    print(
        f"Spike explanations generated: "
        f"{len(explanations)}"
    )

    print("\nMajor airfare movements:")

    for item in explanations:
        print(
            f"{item['date']} | "
            f"Index {item['previous_index']} → "
            f"{item['index']} | "
            f"+{item['index_change_pct']}% | "
            f"{item['severity']}"
        )

        for route in item["top_affected_routes"][:3]:
            print(
                f"   {route['origin']}-"
                f"{route['destination']} "
                f"T+{route['booking_window']}: "
                f"+{route['change_pct']}%"
            )

    print(
        f"\nSaved to {OUTPUT}"
    )


if __name__ == "__main__":
    main()
