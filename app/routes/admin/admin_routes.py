from flask import render_template, redirect, flash, url_for, session
from app.utils.constants import ERROR_PLEASE_LOG_IN


def init_app(app):
    @app.route("/admin/dashboard")
    def admin_dashboard():
        if "username" not in session or session.get("role") != "admin":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return redirect(url_for("index"))

        return render_template(
            "admin_dashboard.html",
            logged_in_user=session["username"],
            role=session["role"],
        )
