import csv
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database import db_connection

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

CSV_FILES = [
    DATA_DIR / "events.csv",
    DATA_DIR / "generated_events.csv",
]


def text_to_bool(value):
    return str(value).strip().lower() in ["true", "1", "yes"]


def import_file(path):
    if not path.exists():
        print(f"Skipping missing file: {path}")
        return

    conn = db_connection()
    cur = conn.cursor()

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cur.execute("""
                INSERT INTO events (
                    title, description, start_time, end_time,
                    source, event_type, location, address, room,
                    organizer, ticket_url, is_free
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                row["title"],
                row["description"],
                row["start_time"],
                row["end_time"],
                row["source"],
                row["event_type"],
                row["location"],
                row["address"],
                row["room"],
                row["organizer"],
                row["ticket_url"],
                text_to_bool(row["is_free"])
            ))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Imported events from {path}")


for csv_file in CSV_FILES:
    import_file(csv_file)