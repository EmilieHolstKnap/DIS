from datetime import datetime, timedelta
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "generated_events.csv"

FIELDNAMES = [
    "title", "description", "start_time", "end_time", "source", "event_type",
    "location", "address", "room", "organizer", "ticket_url", "is_free"
]

events = []


def add_event(title, description, start, end, event_type, is_free):
    events.append({
        "title": title,
        "description": description,
        "start_time": start.strftime("%Y-%m-%d %H:%M"),
        "end_time": end.strftime("%Y-%m-%d %H:%M"),
        "source": "Generated",
        "event_type": event_type,
        "location": "Caféen?",
        "address": "Universitetsparken 15C Copenhagen",
        "room": "",
        "organizer": "Caféen?",
        "ticket_url": "",
        "is_free": str(is_free).lower()
    })


# Weekly Pub Quiz
start = datetime(2026, 6, 9, 19, 0)
for i in range(12):
    s = start + timedelta(days=7 * i)
    add_event(
        "Caféen? Pub Quiz Night",
        "Weekly pub quiz at Caféen",
        s,
        s + timedelta(hours=3),
        "Social",
        False
    )


# Meeple Monday every second Monday
start = datetime(2026, 6, 15, 18, 0)
for i in range(8):
    s = start + timedelta(days=14 * i)
    add_event(
        "Meeple Monday - Board Game Night",
        "Board game night at Caféen",
        s,
        s + timedelta(hours=4),
        "Social",
        True
    )


# Monthly board meetings
start = datetime(2026, 6, 24, 17, 0)
for i in range(6):
    s = start + timedelta(days=30 * i)
    add_event(
        "Bestyrelsesmøde på C?",
        "Board meeting at Caféen",
        s,
        s + timedelta(hours=2),
        "Organization",
        True
    )


with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(events)

print(f"Generated {len(events)} events in {OUTPUT_FILE}")