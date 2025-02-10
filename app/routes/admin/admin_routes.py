from flask import render_template, redirect, flash, url_for, session
from app.utils.constants import (
    ERROR_PLEASE_LOG_IN,
    ERROR_NO_USERS_FOUND,
    ERROR_FETCHING_DATA,
    ERROR_NO_CARS_FOUND,
    ERROR_NO_SERVICES_FOUND,
    EXPORT_CSV_MESSAGE,
)
from app.actions.admin_actions import AdminActions
import logging

admin_actions = AdminActions()


def init_app(app):
    @app.route("/admin/dashboard")
    def admin_dashboard():
        if "username" not in session or session.get("role") != "admin":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return redirect(url_for("index"))

        try:
            total_users = admin_actions.get_total_users()
            total_cars = admin_actions.get_total_cars()

            if total_users is None or total_cars is None:
                raise Exception(ERROR_FETCHING_DATA)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_dashboard.html",
            total_users=total_users,
            total_cars=total_cars,
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

    @app.route("/admin/services")
    def list_services():
        if "username" not in session or session.get("role") != "admin":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return redirect(url_for("index"))
        try:
            services = admin_actions.get_all_services() or []

            if not services:
                flash(ERROR_NO_SERVICES_FOUND, "warning")
                return redirect(url_for("admin_dashboard"))

            for service in services:
                service["mileage"] = (
                    service["mileage"] if service["mileage"] is not None else "N/A"
                )
                service["service_type"] = (
                    service["service_type"] if service["service_type"] else "N/A"
                )
                service["service_date"] = (
                    service["service_date"] if service["service_date"] else "N/A"
                )
                service["next_service_date"] = (
                    service["next_service_date"]
                    if service["next_service_date"]
                    else "N/A"
                )
                service["cost"] = (
                    service["cost"] if service["cost"] is not None else "N/A"
                )
                service["notes"] = service["notes"] if service["notes"] else "N/A"

            return render_template("services.html", services=services, message=EXPORT_CSV_MESSAGE)

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("admin_dashboard"))
