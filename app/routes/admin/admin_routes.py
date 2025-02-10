from flask import render_template, redirect, flash, url_for, session
from app.utils.constants import (
    ERROR_NO_USERS_FOUND,
    ERROR_FETCHING_DATA,
    ERROR_NO_CARS_FOUND,
    ERROR_NO_SERVICES_FOUND,
)
from app.actions.admin_actions import AdminActions
from app.database.database_handler import DatabaseHandler
from app.utils.helpers import Helpers
import logging

logging.basicConfig(level=logging.ERROR)

db_handler = DatabaseHandler()
helpers = Helpers(db_handler)
admin_actions = AdminActions()


def init_app(app):
    @app.route("/admin/dashboard")
    def admin_dashboard():
        if not helpers.check_admin_session():
            return redirect(url_for("index"))

        try:
            total_users = admin_actions.get_total_users()
            total_cars = admin_actions.get_total_cars()
            total_services = admin_actions.get_total_services()

            if None in (total_users, total_cars, total_services):
                raise Exception(ERROR_FETCHING_DATA)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)

        return render_template(
            "admin_dashboard.html",
            total_users=total_users,
            total_cars=total_cars,
            total_services=total_services,
            logged_in_user=session["username"],
            role=session["role"],
        )

    @app.route("/admin/users")
    def list_users():
        if not helpers.check_admin_session():
            return redirect(url_for("index"))

        try:
            users = admin_actions.get_all_users()

            if not users:
                flash(ERROR_NO_USERS_FOUND, "warning")
                return redirect(url_for("admin_dashboard"))

            return render_template("users.html", users=users)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)

    @app.route("/admin/cars")
    def list_cars():
        if not helpers.check_admin_session():
            return redirect(url_for("index"))
        
        try:
            cars = admin_actions.get_all_cars()

            if not cars:
                flash(ERROR_NO_CARS_FOUND, "warning")
                return redirect(url_for("admin_dashboard"))

            return render_template("cars.html", cars=cars)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)

    @app.route("/admin/services")
    def list_services():
        if not helpers.check_admin_session():
            return redirect(url_for("index"))
        
        try:
            services = admin_actions.get_all_services() or []

            if not services:
                flash(ERROR_NO_SERVICES_FOUND, "warning")
                return redirect(url_for("admin_dashboard"))

            for service in services:
                service["mileage"] = service["mileage"] or "N/A"
                service["service_type"] = service["service_type"] or "N/A"
                service["service_date"] = service["service_date"] or "N/A"
                service["next_service_date"] = service["next_service_date"] or "N/A"
                service["cost"] = service["cost"] if service["cost"] is not None else "N/A"
                service["notes"] = service["notes"] or "N/A"

            return render_template(
                "services.html", services=services
            )

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)
