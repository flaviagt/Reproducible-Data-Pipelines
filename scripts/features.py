from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


INPUT = Path("data/transformed/events.csv")
OUTPUT = Path("data/features/events.csv")
FIELDNAMES = [
    "user_id",
    "timestamp",
    "event_type",
    "duration_seconds",
    "date",
    "duration_minutes",
    "weekday",
]


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with INPUT.open(newline="") as input_file, OUTPUT.open("w", newline="") as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for row in reader:
            duration_seconds = int(row["duration_seconds"])
            event_date = datetime.strptime(row["date"], "%Y-%m-%d")
            row["duration_minutes"] = str(duration_seconds / 60)
            row["weekday"] = event_date.strftime("%A")
            writer.writerow(row)


if __name__ == "__main__":
    main()
