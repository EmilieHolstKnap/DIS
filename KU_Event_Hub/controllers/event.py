from flask import Blueprint, render_template, request
from models.event import (
    list_events,
    get_event,
    list_event_types,
    list_organizers
)

bp = Blueprint('event', __name__, url_prefix='/')


@bp.route('/events')
def events():
    selected_type = request.args.get('type')
    selected_organizer = request.args.get('organizer')

    events = list_events(
        event_type=selected_type,
        organizer=selected_organizer
    )

    event_types = list_event_types()
    organizers = list_organizers()

    return render_template(
        'events.html',
        events=events,
        event_types=event_types,
        organizers=organizers,
        selected_type=selected_type,
        selected_organizer=selected_organizer
    )


@bp.route('/events/<int:event_id>')
def event_details(event_id):
    event = get_event(event_id)

    if event is None:
        return "Event not found", 404

    return render_template('event_details.html', event=event)