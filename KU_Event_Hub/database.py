import csv
import psycopg2
import os

# PostgreSQL configuration
user = os.environ.get('PGUSER', 'emilie')
password = os.environ.get('PGPASSWORD', '')
host = os.environ.get('HOST', '127.0.0.1')


def db_connection():
    db = f"dbname='ku_event_hub' user={user} host={host}"
    return psycopg2.connect(db)


def init_db():
    conn = db_connection()
    cur = conn.cursor()

    # =====================
    # CREATE TABLES
    # =====================

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS event_types (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            address TEXT,
            room TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,

            source_id INTEGER REFERENCES sources(id),
            event_type_id INTEGER REFERENCES event_types(id),
            location_id INTEGER REFERENCES locations(id),

            organizer TEXT,
            ticket_url TEXT,
            is_free BOOLEAN,

            UNIQUE(title, start_time, location_id)
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

    # =====================
    # IMPORT CSV DATA
    # =====================

    csv_files = [
        "data/events.csv",
        "data/generated_events.csv"
    ]

    for csv_path in csv_files:

        try:
            with open(csv_path, encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:

                    # Insert source
                    cur.execute(
                        """
                        INSERT INTO sources(name)
                        VALUES (%s)
                        ON CONFLICT DO NOTHING
                        """,
                        (row["source"],)
                    )

                    # Insert event type
                    cur.execute(
                        """
                        INSERT INTO event_types(name)
                        VALUES (%s)
                        ON CONFLICT DO NOTHING
                        """,
                        (row["event_type"],)
                    )

                    # Insert location
                    cur.execute(
                        """
                        INSERT INTO locations(name, address, room)
                        VALUES (%s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (
                            row["location"],
                            row["address"],
                            row["room"]
                        )
                    )

                    # Insert event
                    cur.execute(
                        """
                        INSERT INTO events
                        (
                            title,
                            description,
                            start_time,
                            end_time,
                            source_id,
                            event_type_id,
                            location_id,
                            organizer,
                            ticket_url,
                            is_free
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            %s,
                            (SELECT id FROM sources WHERE name=%s),
                            (SELECT id FROM event_types WHERE name=%s),
                            (SELECT id FROM locations WHERE name=%s),
                            %s,
                            %s,
                            %s
                        )
                        ON CONFLICT DO NOTHING
                        """,
                        (
                            row["title"],
                            row["description"],
                            row["start_time"],
                            row["end_time"],
                            row["source"],
                            row["event_type"],
                            row["location"],
                            row["organizer"],
                            row["ticket_url"],
                            row["is_free"].lower() == "true"
                        )
                    )

            print(f"Imported events from {csv_path}")

        except FileNotFoundError:
            print(f"{csv_path} not found. Skipping.")

    conn.commit()
    print("Events loaded successfully.")

    cur.close()
    conn.close()