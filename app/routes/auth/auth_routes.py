from flask import render_template, request, redirect, flash, url_for, session
from app.utils.constants import ERROR_USER_NOT_FOUND


def init_app(app, login):
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if login.authenticate(username, password):
                session["role"] = login.role
                return redirect(
                    url_for(
                        "admin_dashboard" if login.role == "admin" else "user_dashboard"
                    )
                )
            else:
                flash(ERROR_USER_NOT_FOUND, "error")
                return redirect(url_for("index"))

        return render_template("index.html")
