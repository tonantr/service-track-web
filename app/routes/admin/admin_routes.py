from flask import render_template, redirect, flash, url_for, session
from app.utils.constants import (
    ERROR_PLEASE_LOG_IN,
    ERROR_NO_USERS_FOUND,
    ERROR_FETCHING_DATA,
    ERROR_NO_CARS_FOUND,
)
from app.actions.admin_actions import AdminActions


admin_actions = AdminActions()


def init_app(app):
    @app.route("/admin/dashboard")
    def admin_dashboard():
        if "username" not in session or session.get("role") != "admin":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return redirect(url_for("index"))

        try:
            total_users = admin_actions.get_total_users()

            if total_users is None:
                total_users = ERROR_FETCHING_DATA
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            total_users = ERROR_FETCHING_DATA

        return render_template(
            "admin_dashboard.html",
            total_users=total_users,
            logged_in_user=session["username"],
            role=session["role"],
        )

    @app.route("/admin/users")
    def list_users():
        if "username" not in session or session.get("role") != "admin":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return redirect(url_for("index"))

        try:
            users = admin_actions.get_all_users()

            if not users:
                flash(ERROR_NO_USERS_FOUND, "warning")
                return redirect(url_for("admin_dashboard"))

            return render_template("users.html", users=users)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("admin_dashboard"))


    @app.route("/admin/cars")
    def list_cars():
        if "username" not in session or session.get("role") != "admin":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return redirect(url_for("index"))
        try:
            cars = admin_actions.get_all_cars()

            if not cars:
                flash(ERROR_NO_CARS_FOUND, "warning")
                return redirect(url_for("admin_dashboard"))
            
            return render_template("cars.html", cars=cars)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("admin_dashboard"))