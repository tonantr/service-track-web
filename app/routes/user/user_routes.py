from flask import render_template, redirect, flash, url_for, session
from app.utils.constants import ERROR_PLEASE_LOG_IN


def init_app(app):
    @app.route("/user/dashboard")
    def user_dashboard():
        if "username" not in session or session.get("role") != "user":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return redirect(url_for("index"))

        return render_template(
            "user_dashboard.html",
            logged_in_user=session["username"],
            role=session["role"],
        )
