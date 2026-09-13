import json
from pathlib import Path
from statistics import mean, stdev

from src.index_engine import load_observations, calculate_daily_index


INPUT = Path("data/raw/backtest_airfares.json")
OUTPUT = Path("data/processed/anomalies.json")


def detect_anomalies(daily_results, window=7, threshold=2.0):
    """
    Detect unusually high airfare-index values using
    a rolling z-score.

    A positive z-score above the threshold indicates
    an unusually high index relative to its recent history.
    """

    results = []

    for i, current in enumerate(daily_results):

        start = max(0, i - window)

        previous = [
            item["index"]
            for item in daily_results[start:i]
        ]

        if len(previous) < 3:
            results.append({
                **current,
                "z_score": None,
                "anomaly": False,
            })
            continue

        baseline = mean(previous)
        deviation = stdev(previous)

        if deviation == 0:
            z_score = 0
        else:
            z_score = (
                current["index"] - baseline
            ) / deviation

        anomaly = z_score >= threshold

        results.append({
            **current,
            "baseline": round(baseline, 4),
            "z_score": round(z_score, 4),
            "anomaly": anomaly,
        })

    return results


def main():

    observations = load_observations(str(INPUT))

    daily_results = calculate_daily_index(
        observations
    )

    anomalies = detect_anomalies(
        daily_results
    )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT, "w") as f:
        json.dump(
            anomalies,
            f,
            indent=2
        )

    detected = [
        item
        for item in anomalies
        if item["anomaly"]
    ]

    print(
        f"Analysed {len(anomalies)} daily index points"
    )

    print(
        f"Anomalies detected: {len(detected)}"
    )

    print("\nDetected airfare surges:")

    for item in detected:
        print(
            f"{item['date']} | "
            f"Index: {item['index']} | "
            f"Z-score: {item['z_score']}"
        )

    print(
        f"\nSaved results to {OUTPUT}"
    )


if __name__ == "__main__":
    main()
