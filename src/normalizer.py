import json
from pathlib import Path

from src.models import AirfareObservation
from src.routes import BOOKING_WINDOWS


VALID_STATUSES = {
    "available",
    "sold_out",
    "cancelled",
}


def validate_observation(observation: AirfareObservation) -> list[str]:
    errors = []

    if observation.origin == observation.destination:
        errors.append("Origin and destination cannot be the same")

    if observation.booking_window not in BOOKING_WINDOWS:
        errors.append(
            f"Invalid booking window: {observation.booking_window}"
        )

    if observation.total_fare <= 0:
        errors.append("Total fare must be greater than zero")

    if observation.base_fare is not None and observation.base_fare < 0:
        errors.append("Base fare cannot be negative")

    if observation.taxes is not None and observation.taxes < 0:
        errors.append("Taxes cannot be negative")

    if observation.fees is not None and observation.fees < 0:
        errors.append("Fees cannot be negative")

    if observation.availability_status not in VALID_STATUSES:
        errors.append(
            f"Invalid availability status: "
            f"{observation.availability_status}"
        )

    # Check fare decomposition when all components are available.
    if (
        observation.base_fare is not None
        and observation.taxes is not None
        and observation.fees is not None
    ):
        components = (
            observation.base_fare
            + observation.taxes
            + observation.fees
        )

        if abs(components - observation.total_fare) > 1:
            errors.append(
                "Base fare + taxes + fees does not match total fare"
            )

    return errors


def validate_raw_file(path: str):
    with open(path, "r") as f:
        raw_data = json.load(f)

    valid = []
    invalid = []

    for item in raw_data:
        try:
            observation = AirfareObservation.model_validate(item)
            errors = validate_observation(observation)

            if errors:
                invalid.append(
                    {
                        "observation": item,
                        "errors": errors,
                    }
                )
            else:
                valid.append(observation)

        except Exception as exc:
            invalid.append(
                {
                    "observation": item,
                    "errors": [str(exc)],
                }
            )

    return valid, invalid


if __name__ == "__main__":
    input_path = Path("data/raw/demo_airfares.json")

    valid, invalid = validate_raw_file(str(input_path))

    print(f"Total observations: {len(valid) + len(invalid)}")
    print(f"Valid observations: {len(valid)}")
    print(f"Invalid observations: {len(invalid)}")
