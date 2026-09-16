from typing import Dict, List

from src.routes import ROUTES, BOOKING_WINDOWS


def equal_route_weights() -> Dict[str, float]:
    """
    Temporary MVP fallback.

    Each route receives equal weight until validated passenger-traffic
    data is added. This keeps the methodology explicit rather than
    inventing traffic figures.
    """
    weight = 1.0 / len(ROUTES)

    return {
        f"{route['origin']}-{route['destination']}": weight
        for route in ROUTES
    }


def equal_booking_window_weights() -> Dict[int, float]:
    """
    Temporary MVP fallback.

    Each booking window receives equal weight until empirical
    booking-share data is available.
    """
    weight = 1.0 / len(BOOKING_WINDOWS)

    return {
        window: weight
        for window in BOOKING_WINDOWS
    }


def validate_weights(weights: Dict) -> bool:
    """Check that weights are non-negative and sum to approximately 1."""
    if not weights:
        return False

    if any(value < 0 for value in weights.values()):
        return False

    return abs(sum(weights.values()) - 1.0) < 1e-9


def build_stratum_weights() -> List[dict]:
    """
    Build explicit route × booking-window strata.

    Route and booking-window weights are currently equal-weight
    fallbacks. The structure is ready for real empirical weights.
    """
    route_weights = equal_route_weights()
    window_weights = equal_booking_window_weights()

    strata = []

    for route in ROUTES:
        route_key = f"{route['origin']}-{route['destination']}"

        for window in BOOKING_WINDOWS:
            route_weight = route_weights[route_key]
            window_weight = window_weights[window]

            strata.append(
                {
                    "origin": route["origin"],
                    "destination": route["destination"],
                    "route": route_key,
                    "booking_window": window,
                    "route_weight": route_weight,
                    "booking_window_weight": window_weight,
                    "combined_weight": route_weight * window_weight,
                }
            )

    return strata


if __name__ == "__main__":
    route_weights = equal_route_weights()
    window_weights = equal_booking_window_weights()
    strata = build_stratum_weights()

    print("AERIS weighting layer")
    print("---------------------")

    print("\nRoute weights:")
    for route, weight in route_weights.items():
        print(f"{route}: {weight:.6f}")

    print("\nBooking-window weights:")
    for window, weight in window_weights.items():
        print(f"T+{window}: {weight:.6f}")

    print(f"\nStrata generated: {len(strata)}")

    total_weight = sum(item["combined_weight"] for item in strata)
    print(f"Total stratum weight: {total_weight:.6f}")

    print(
        "Route weights valid:",
        validate_weights(route_weights),
    )
    print(
        "Booking-window weights valid:",
        validate_weights(window_weights),
    )
