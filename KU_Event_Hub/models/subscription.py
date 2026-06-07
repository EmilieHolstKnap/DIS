from database import db_connection


def subscribe_organizer(user_id, organizer):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO organizer_subscriptions(user_id, organizer)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (user_id, organizer))

    conn.commit()
    cur.close()
    conn.close()


def unsubscribe_organizer(user_id, organizer):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM organizer_subscriptions
        WHERE user_id = %s
        AND organizer = %s
    """, (user_id, organizer))

    conn.commit()
    cur.close()
    conn.close()


def is_organizer_subscribed(user_id, organizer):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1
        FROM organizer_subscriptions
        WHERE user_id = %s
        AND organizer = %s
    """, (user_id, organizer))

    subscribed = cur.fetchone() is not None

    cur.close()
    conn.close()

    return subscribed