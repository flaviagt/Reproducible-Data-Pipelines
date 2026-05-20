from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


INPUT = Path("data/raw/events.csv")
OUTPUT = Path("data/clean/events.csv")
VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}
TIMESTAMP_FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
)
FIELDNAMES = ["user_id", "timestamp", "event_type", "duration_seconds"]


def parse_timestamp(value: str) -> str | None:
    for timestamp_format in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(value, timestamp_format).strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    return None


def clean_row(row: dict[str, str]) -> dict[str, str] | None:
    if any(not row.get(field, "").strip() for field in FIELDNAMES):
        return None

    event_type = row["event_type"].strip()
    if event_type not in VALID_EVENT_TYPES:
        return None

    try:
        duration_seconds = int(row["duration_seconds"])
    except ValueError:
        return None
    if duration_seconds <= 0:
        return None

    timestamp = parse_timestamp(row["timestamp"].strip())
    if timestamp is None:
        return None

    return {
        "user_id": row["user_id"].strip(),
        "timestamp": timestamp,
        "event_type": event_type,
        "duration_seconds": str(duration_seconds),
    }


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with INPUT.open(newline="") as input_file, OUTPUT.open("w", newline="") as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for row in reader:
            cleaned = clean_row(row)
            if cleaned is not None:
                writer.writerow(cleaned)


if __name__ == "__main__":
    main()
