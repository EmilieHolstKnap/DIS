from database import db_connection


class Event:
    def __init__(
        self,
        id,
        title,
        description,
        start_time,
        source,
        event_type,
        location
    ):
        self.id = id
        self.title = title
        self.description = description
        self.start_time = start_time
        self.source = source
        self.event_type = event_type
        self.location = location


def list_events():
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            events.id,
            events.title,
            events.description,
            events.start_time,
            sources.name,
            event_types.name,
            locations.name
        FROM events
        JOIN sources
            ON events.source_id = sources.id
        JOIN event_types
            ON events.event_type_id = event_types.id
        JOIN locations
            ON events.location_id = locations.id
        ORDER BY events.start_time
    """)

    db_events = cur.fetchall()

    events = []

    for event in db_events:
        events.append(
            Event(
                event[0],  # id
                event[1],  # title
                event[2],  # description
                event[3],  # start_time
                event[4],  # source
                event[5],  # event_type
                event[6]   # location
            )
        )

    cur.close()
    conn.close()

    return events