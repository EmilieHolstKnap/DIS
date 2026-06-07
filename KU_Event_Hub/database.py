import csv
import os
import psycopg2


user = os.getenv("PGUSER", "postgres")
password = os.getenv("PGPASSWORD", "123")
host = os.getenv("PGHOST", "127.0.0.1")
database = os.getenv("PGDATABASE", "ku_event_hub")
port = os.getenv("PGPORT", "5432")


def db_connection():
    return psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host,
        port=port
    )


def init_db():
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS event_types (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            organizer TEXT,
            event_type_id INTEGER REFERENCES event_types(id),
            location TEXT,
            ticket_url TEXT,
            is_free BOOLEAN,
            UNIQUE(title, start_time, location)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_events (
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
            PRIMARY KEY(user_id, event_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizer_subscriptions (
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            organizer TEXT NOT NULL,
            PRIMARY KEY(user_id, organizer)
        )
    """)

    conn.commit()

    csv_files = [
        "data/events.csv",
        "data/generated_events.csv"
    ]

    for csv_path in csv_files:
        try:
            with open(csv_path, encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    cur.execute("""
                        INSERT INTO event_types(name)
                        VALUES (%s)
                        ON CONFLICT DO NOTHING
                    """, (row["event_type"],))

                    cur.execute("""
                        INSERT INTO events (
                            title,
                            description,
                            start_time,
                            end_time,
                            organizer,
                            event_type_id,
                            location,
                            ticket_url,
                            is_free
                        )
                        VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            (SELECT id FROM event_types WHERE name = %s),
                            %s,
                            %s,
                            %s
                        )
                        ON CONFLICT DO NOTHING
                    """, (
                        row["title"],
                        row["description"],
                        row["start_time"],
                        row["end_time"],
                        row["organizer"],
                        row["event_type"],
                        row["location"],
                        row["ticket_url"],
                        row["is_free"].lower() == "true"
                    ))

            print(f"Imported events from {csv_path}")

        except FileNotFoundError:
            print(f"{csv_path} not found. Skipping.")

    conn.commit()
    print("Events loaded successfully.")

    cur.close()
    conn.close()