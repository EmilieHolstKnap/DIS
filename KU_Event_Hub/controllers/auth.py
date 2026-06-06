from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user import create_user, check_login

bp = Blueprint("auth", __name__, url_prefix="/")

@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        action = request.form["action"]

        if action == "register":
            user = create_user(username, password)

            if user:
                session["user_id"] = user[0]
                session["username"] = user[1]
                return redirect(url_for("event.events"))
            else:
                error = "Username already exists."

        elif action == "login":
            user = check_login(username, password)

            if user:
                session["user_id"] = user[0]
                session["username"] = user[1]
                return redirect(url_for("event.events"))
            else:
                error = "Invalid username or password."

    return render_template(
        "pages/login.html",
        error=error
    )

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("event.home"))