from database import db_connection

def save_event(user_id, event_id):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO saved_events(user_id, event_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (user_id, event_id))

    conn.commit()
    conn.close()

def get_saved_events(user_id):

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT e.*
        FROM events e
        JOIN saved_events s
          ON e.id = s.event_id
        WHERE s.user_id = %s
    """, (user_id,))

    events = cur.fetchall()

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
    conn.close()