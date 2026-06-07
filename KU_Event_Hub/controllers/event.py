from flask import Blueprint, render_template, request, session, redirect, url_for

from models.event import (
    list_events,
    get_event,
    list_event_types,
    list_organizers,
    list_events_grouped_by_organizer
)
from models.saved_event import (
    save_event,
    get_saved_events,
    remove_saved_event,
    is_event_saved
)
from models.subscription import (
    subscribe_organizer,
    unsubscribe_organizer,
    is_organizer_subscribed,
    get_subscribed_organizers
)


bp = Blueprint("event", __name__, url_prefix="/")


def login_required():
    return "user_id" in session


def redirect_back(default_route):
    next_page = request.form.get("next")

    if next_page:
        return redirect(next_page)

    return redirect(url_for(default_route))


@bp.route("/")
def home():
    return render_template("pages/home.html")


@bp.route("/events")
def events():
    selected_type = request.args.get("type")
    selected_organizer = request.args.get("organizer")

    events = list_events(
        event_type=selected_type,
        organizer=selected_organizer
    )

    return render_template(
        "pages/events.html",
        events=events,
        event_types=list_event_types(),
        organizers=list_organizers(),
        selected_type=selected_type,
        selected_organizer=selected_organizer
    )


@bp.route("/events/<int:event_id>")
def event_details(event_id):
    event = get_event(event_id)

    if event is None:
        return "Event not found", 404

    saved = False
    subscribed = False

    if login_required():
        saved = is_event_saved(session["user_id"], event_id)
        subscribed = is_organizer_subscribed(
            session["user_id"],
            event.organizer
        )

    return render_template(
        "pages/event_details.html",
        event=event,
        saved=saved,
        subscribed=subscribed
    )


@bp.route("/events/<int:event_id>/save", methods=["POST"])
def save(event_id):
    if not login_required():
        return redirect(url_for("auth.login"))

    save_event(session["user_id"], event_id)

    return redirect(url_for("event.event_details", event_id=event_id))


@bp.route("/events/<int:event_id>/unsave", methods=["POST"])
def unsave(event_id):
    if not login_required():
        return redirect(url_for("auth.login"))

    remove_saved_event(session["user_id"], event_id)

    return redirect_back("event.my_events")


@bp.route("/my-events")
def my_events():
    if not login_required():
        return redirect(url_for("auth.login"))

    events = get_saved_events(session["user_id"])
    subscribed_organizers = get_subscribed_organizers(session["user_id"])

    return render_template(
        "pages/my_events.html",
        events=events,
        subscribed_organizers=subscribed_organizers
    )


@bp.route("/organizers")
def organizers():
    grouped_events = list_events_grouped_by_organizer()

    return render_template(
        "pages/organizers.html",
        grouped_events=grouped_events
    )


@bp.route("/organizers/<organizer>/subscribe", methods=["POST"])
def subscribe(organizer):
    if not login_required():
        return redirect(url_for("auth.login"))

    subscribe_organizer(session["user_id"], organizer)

    return redirect_back("event.events")


@bp.route("/organizers/<organizer>/unsubscribe", methods=["POST"])
def unsubscribe(organizer):
    if not login_required():
        return redirect(url_for("auth.login"))

    unsubscribe_organizer(session["user_id"], organizer)

    return redirect_back("event.events")