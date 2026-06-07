from database import db_connection


class Event:
    def __init__(
        self,
        id,
        title,
        description,
        start_time,
        end_time,
        organizer,
        event_type,
        location,
        ticket_url,
        is_free
    ):
        self.id = id
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.organizer = organizer
        self.event_type = event_type
        self.location = location
        self.ticket_url = ticket_url
        self.is_free = is_free


def list_events(event_type=None, organizer=None):
    conn = db_connection()
    cur = conn.cursor()

    query = """
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
        JOIN event_types
            ON events.event_type_id = event_types.id
    """

    conditions = []
    params = []

    if event_type:
        conditions.append("event_types.name = %s")
        params.append(event_type)

    if organizer:
        conditions.append("events.organizer = %s")
        params.append(organizer)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY events.start_time"

    cur.execute(query, params)

    events = [Event(*row) for row in cur.fetchall()]

    cur.close()
    conn.close()

    return events


def get_event(event_id):
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
        JOIN event_types
            ON events.event_type_id = event_types.id
        WHERE events.id = %s
    """, (event_id,))

    event = cur.fetchone()

    cur.close()
    conn.close()

    if event is None:
        return None

    return Event(*event)


def list_event_types():
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name
        FROM event_types
        ORDER BY name
    """)

    event_types = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return event_types


def list_organizers():
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT organizer
        FROM events
        WHERE organizer IS NOT NULL
        AND organizer != ''
        ORDER BY organizer
    """)

    organizers = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return organizers


def list_events_grouped_by_organizer():
    events = list_events()
    grouped_events = {}

    for event in events:
        organizer = event.organizer or "Unknown organizer"

        if organizer not in grouped_events:
            grouped_events[organizer] = []

        grouped_events[organizer].append(event)

    return grouped_events