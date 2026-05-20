from __future__ import annotations

import csv
from pathlib import Path


INPUT = Path("data/clean/events.csv")
OUTPUT = Path("data/transformed/events.csv")
FIELDNAMES = ["user_id", "timestamp", "event_type", "duration_seconds", "date"]


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with INPUT.open(newline="") as input_file, OUTPUT.open("w", newline="") as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for row in reader:
            row["date"] = row["timestamp"][:10]
            writer.writerow(row)


if __name__ == "__main__":
    main()
