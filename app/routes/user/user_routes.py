from flask import render_template, redirect, flash, url_for, session
from app.utils.constants import (
    ERROR_NO_USERS_FOUND,
    ERROR_USER_NOT_FOUND,
    ERROR_FETCHING_DATA,
    ERROR_NO_CARS_FOUND,
    ERROR_CAR_NOT_FOUND,
    ERROR_NO_SERVICES_FOUND,
    ERROR_SERVICE_NOT_FOUND
)
from app.actions.user_actions import UserActions
from app.database.database_handler import DatabaseHandler
from app.utils.helpers import Helpers
from app.utils.validators import validate_email, validate_password, validate_username
from app.auth.password_hashing import hash_password
import logging
import os
import csv

logging.basicConfig(level=logging.ERROR)

db_handler = DatabaseHandler()
helpers = Helpers(db_handler)
user_actions = UserActions()

def init_app(app):
    @app.route("/user/dashboard")
    def user_dashboard():
        if not Helpers.check_user_session():
            return redirect(url_for("index"))
        
        try:
            user = helpers.get_user_by_username(session["username"])
            if not user:
                flash(ERROR_USER_NOT_FOUND, "danger")
                return redirect(url_for("index"))

            cars = user_actions.get_cars_by_user_id(user["user_id"])
            if cars is None:
                cars = []

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)

        return render_template(
            "user/user_dashboard.html",
            cars=cars,
            logged_in_user=session["username"],
            role=session["role"],
        )

    @app.route("/user/cars")
    def get_cars():
        if not Helpers.check_user_session():
            return redirect(url_for("index"))
        
        try:
            user = helpers.get_user_by_username(session["username"])
            if not user:
                flash(ERROR_USER_NOT_FOUND, "danger")
                return redirect(url_for("index"))

            cars = user_actions.get_cars_by_user_id(user["user_id"])
            if cars is None:
                cars = []

            return render_template("user/user_cars.html", cars=cars)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)