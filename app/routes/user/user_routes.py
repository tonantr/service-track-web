from flask import render_template, redirect, flash, url_for, session, request, send_file
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

            cars = user_actions.get_cars_by_user(user["user_id"])
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

            cars = user_actions.get_cars_by_user(user["user_id"]) or []
            return render_template("user/user_cars.html", cars=cars)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)
    
    @app.route("/user/profile")
    def get_profile():
        if not Helpers.check_user_session():
            return redirect(url_for("index"))
        
        try:
            user = helpers.get_user_by_username(session["username"])
            if not user:
                flash(ERROR_USER_NOT_FOUND, "danger")
                return redirect(url_for("index"))
            
            return render_template("user/user_profile.html", user=user)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)
    
    @app.route("/user/profile/update", methods=["GET", "POST"])
    def update_profile():
        if not Helpers.check_user_session():
            return redirect(url_for("index"))
        
        user_id = session.get("user_id")
        user = helpers.get_user_by_id(user_id)
        if not user:
            flash(ERROR_USER_NOT_FOUND, "warning")
            return redirect(url_for("get_profile"))
        
        if request.method == "POST":
            try:
                form_data = {
                    "username": request.form.get("username"),
                    "email": request.form.get("email"),
                    "password": request.form.get("password")
                }

                if request.form.get("username") != user["username"] and helpers.check_username_exists(form_data["username"]):
                        flash("Username already exists.", "warning")
                        return render_template("user/update_profile.html", user=user)
                
                if request.form.get("email") != user["email"] and helpers.check_email_exists(form_data["email"]):
                        flash("Email already exists.", "warning")
                        return render_template("user/update_profile.html", user=user)
                
                if form_data["password"]:
                    form_data["password"] = hash_password(form_data["password"])
                
                if not user_actions.update_user(user_id, **form_data):
                    flash("Failed to update profile.", "danger")
                    return render_template("user/update_profile.html", user=user)
                
                return redirect(url_for("get_profile")) 
            
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)
        
        return render_template("user/update_profile.html", user=user)
    
    @app.route("/user/services", methods=["GET", "POST"])
    def service_history():
        if not Helpers.check_user_session():
            return redirect(url_for("index"))
        
        try:
            cars = user_actions.get_cars_by_user(session["user_id"]) or []

            services = []
            car_id = None

            if request.method == "POST":

                car_id = request.form.get("car_id")

                if car_id:
                    services = user_actions.get_services_by_car(car_id)
                   
                    for service in services:
                        service["mileage"] = service["mileage"] or "N/A"
                        service["service_type"] = service["service_type"] or "N/A"
                        service["service_date"] = service["service_date"] or "N/A"
                        service["next_service_date"] = service["next_service_date"] or "N/A"
                        service["cost"] = service["cost"] if service["cost"] is not None else "N/A"
                        service["notes"] = service["notes"] or "N/A"

            return render_template("user/user_services.html", cars=cars, services=services)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)
    
    @app.route("/user/cars/update/<int:car_id>", methods=["GET", "POST"])
    def edit_car(car_id):
        if not Helpers.check_user_session():
            return redirect(url_for("index"))
        
        car = helpers.get_car_by_id(car_id)
        if not car:
            flash(ERROR_CAR_NOT_FOUND, "danger")
            return redirect(url_for("get_cars"))
        
        if car["user_id"] != session["user_id"]:
            return redirect(url_for("get_cars"))

        if request.method == "POST":
            try:
                form_data = {
                    "user_id": session["user_id"],
                    "name": request.form.get("name"),
                    "model": request.form.get("model"),
                    "year": request.form.get("year"),
                    "vin": request.form.get("vin")
                }

                if not user_actions.update_car(car_id, **form_data):
                    flash("Failed to update car.", "danger")
                    return render_template("user/edit_car.html", car=car)
                
                return redirect(url_for("get_cars"))
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)
        
        return render_template("user/edit_car.html", car=car)
    
    @app.route("/user/<entity>/delete/<int:item_id>", methods=["GET", "POST"])
    def remove_entity(entity, item_id):
        if not Helpers.check_user_session():
            return redirect(url_for("index"))
        
        if entity == "cars":
            item = helpers.get_car_by_id(item_id)
            entity_name = "Car"
        elif entity == "services":
            item = helpers.get_service_by_id(item_id)
            entity_name = "Service"
                
        if not item:
            flash(f"{entity_name} not found.", "warning")
            return redirect(url_for("get_cars")) if entity=="cars" else redirect(url_for("service_history"))
        
        if request.method == "POST":
            try:
                if entity == "cars":
                    if not user_actions.delete_car(item_id):
                        flash("Failed to delete car.", "danger")
                        return redirect(url_for("get_cars"))
                elif entity == "services":
                    pass

                return redirect(url_for("get_cars")) if entity=="cars" else redirect(url_for("service_history"))
            
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)
        
        return render_template("user/remove_entity.html", entity=entity, item=item, entity_name=entity_name)

    @app.route("/user/export/csv", methods=["GET", "POST"])
    def export_to_csv(export_type="cars"):
        if not Helpers.check_user_session():
            return redirect(url_for("index"))
        
        cars = user_actions.get_cars_by_user(session["user_id"])
        
        if request.method == "POST":
            export_type = request.form.get("export_type")
            car_id = request.form.get("car_id")

            if export_type == "services" and not car_id:
                flash("Please select a car to export services.", "warning")
                return redirect(url_for("export_to_csv", export_type=export_type))

            downloads_folder = Helpers.get_downloads_folder()
            file_name = f"{export_type}_usr.csv"
            file_path = os.path.join(downloads_folder, file_name)

            try:
                data, headers = [], []
                if export_type == "cars":
                    data = cars
                    headers = ["CarID", "UserID", "Name", "Model", "Year", "VIN"]
                elif export_type == "services":
                    data = user_actions.get_services_by_car(car_id)
                    headers = ["ID", "Car Name", "Mileage", "Service Type", "Service Date", "Next Service Date", "Cost", "Notes"]

                if not data:
                    flash("No data found", "warning")
                    return redirect(url_for("export_to_csv", export_type=export_type))

                with open(file_path, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    for row in data:
                        writer.writerow(row.values())

                return send_file(file_path, as_attachment=True)
                
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)
        
        return render_template("user/export_to_csv.html", export_type=export_type, cars=cars)

        
        