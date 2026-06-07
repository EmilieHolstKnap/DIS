from database import db_connection
from models.event import Event


def save_event(user_id, event_id):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO saved_events(user_id, event_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (user_id, event_id))

    conn.commit()
    cur.close()
    conn.close()


def get_saved_events(user_id):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            events.id,
            events.title,
            events.description,
            events.start_time,
            events.end_time,
            events.organizer,
            event_types.name,
            events.location,
            events.ticket_url,
            events.is_free
        FROM events
        JOIN saved_events
            ON events.id = saved_events.event_id
        JOIN event_types
            ON events.event_type_id = event_types.id
        WHERE saved_events.user_id = %s
        ORDER BY events.start_time
    """, (user_id,))

    events = [Event(*row) for row in cur.fetchall()]

    cur.close()
    conn.close()

    return events


def remove_saved_event(user_id, event_id):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM saved_events
        WHERE user_id = %s
        AND event_id = %s
    """, (user_id, event_id))

    conn.commit()
    cur.close()
    conn.close()


def is_event_saved(user_id, event_id):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1
        FROM saved_events
        WHERE user_id = %s
        AND event_id = %s
    """, (user_id, event_id))

    saved = cur.fetchone() is not None

    cur.close()
    conn.close()

    return saved