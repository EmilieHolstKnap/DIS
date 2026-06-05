from flask import Blueprint, render_template
from models.event import list_events

bp = Blueprint('event', __name__, url_prefix='/')


@bp.route('/events')
def events():
    events = list_events()
    return render_template('events.html', events=events)