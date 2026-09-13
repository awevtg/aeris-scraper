import json
from pathlib import Path
from datetime import date, timedelta

from src.collectors.demo_collector import collect_demo_fare
from src.routes import ROUTES, BOOKING_WINDOWS


OUTPUT = Path("data/raw/demo_airfares.json")


def main():
    observations = []

    travel_date = date.today() + timedelta(days=30)

    for route in ROUTES:
        for booking_window in BOOKING_WINDOWS:

            fare = 4000 + (
                len(route["origin"]) * 100
                + len(route["destination"]) * 150
                + booking_window * 20
            )

            observation = collect_demo_fare(
                origin=route["origin"],
                destination=route["destination"],
                carrier="DEMO",
                travel_date=travel_date.isoformat(),
                booking_window=booking_window,
                total_fare=float(fare),
            )

            observations.append(observation.model_dump(mode="json"))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w") as f:
        json.dump(observations, f, indent=2)

    print(f"Saved {len(observations)} observations to {OUTPUT}")


if __name__ == "__main__":
    main()
