from flask import render_template, redirect, flash, url_for, request, session, send_file
from app.utils.constants import (
    ERROR_NO_USERS_FOUND,
    ERROR_USER_NOT_FOUND,
    ERROR_FETCHING_DATA,
    ERROR_NO_CARS_FOUND,
    ERROR_CAR_NOT_FOUND,
    ERROR_NO_SERVICES_FOUND,
    ERROR_SERVICE_NOT_FOUND
)
from app.actions.admin_actions import AdminActions
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
admin_actions = AdminActions()


def init_app(app):
    @app.route("/admin/dashboard")
    def admin_dashboard():
        if not Helpers.check_admin_session():
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
            "admin/admin_dashboard.html",
            total_users=total_users,
            total_cars=total_cars,
            total_services=total_services,
            logged_in_user=session["username"],
            role=session["role"],
        )

    @app.route("/admin/users")
    def list_users():
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))

        try:
            users = admin_actions.get_all_users()
            if not users:
                flash(ERROR_NO_USERS_FOUND, "warning")
                return redirect(url_for("admin_dashboard"))

            return render_template("admin/users.html", users=users)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)

    @app.route("/admin/users/add", methods=["GET", "POST"])
    def add_user():
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))
        
        if request.method == "POST":
            try:
                username = request.form.get("username")
                role = request.form.get("role")
                email = request.form.get("email")
                password = request.form.get("password")

                if not validate_username(username):
                    flash("Username must be at least 3 characters.", "danger")
                    return render_template("add_user.html")
                
                if not validate_email(email):
                    flash("Invalid email format.", "danger")
                    return render_template("add_user.html")
                
                if not validate_password(password):
                    flash("Password must be at least 6 characters.", "danger")
                    return render_template("add_user.html")

                if helpers.check_if_username_or_email_exists(username, email):
                    flash("Username or Email already exists.", "warning")
                    return render_template("add_user.html")
                
                if password:
                    hashed_password = hash_password(password)

                if not admin_actions.add_user(username, email, hashed_password, role):
                    flash("Failed to add user.", "danger")
                    return render_template("add_user.html")
                
                return redirect(url_for("list_users")) 
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)
        
        return render_template("admin/add_user.html")

    @app.route("/admin/users/update/<int:user_id>", methods=["GET", "POST"])
    def update_user(user_id):
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))
        
        user = helpers.get_user_by_id(user_id)
        if not user:
            flash(ERROR_USER_NOT_FOUND, "warning")
            return redirect(url_for("list_users"))
        
        if request.method == "POST":
            try:
                updated_data = {
                    "username": request.form.get("username"),
                    "role": request.form.get("role"),
                    "email": request.form.get("email"),
                    "password": request.form.get("password")
                }

                if helpers.check_if_username_or_email_exists(updated_data["username"], updated_data["email"], exclude_user_id=user["user_id"]):
                    flash("Username or Email already exists.", "warning")
                    return render_template("update_user.html", user=user)
                
                if updated_data["password"]:
                    updated_data["password"] = hash_password(updated_data["password"])
                

                if not admin_actions.update_user(user_id, **updated_data):
                    flash("Failed to update user.", "danger")
                    return render_template("update_user.html")
                
                return redirect(url_for("list_users")) 
            
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)
        
        return render_template("update_user.html", user=user)
      
    @app.route("/admin/cars")
    def list_cars():
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))
        
        try:
            cars = admin_actions.get_all_cars()

            if not cars:
                flash(ERROR_NO_CARS_FOUND, "warning")
                return redirect(url_for("admin_dashboard"))

            return render_template("admin/cars.html", cars=cars)
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)

    @app.route("/admin/cars/add", methods=["GET", "POST"])
    def add_car():
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))
        
        users = admin_actions.get_all_users()
        if not users:
                flash(ERROR_NO_USERS_FOUND, "warning")
                return redirect(url_for("list_cars"))
        
        if request.method == "POST":
            try:
                form_data = {
                    "user_id": request.form.get("user_id"),
                    "name": request.form.get("name"),
                    "model": request.form.get("model"),
                    "year": request.form.get("year"),
                    "vin": request.form.get("vin")
                }

                if helpers.check_vin_exists(form_data["vin"]):
                    flash("VIN already exists.", "warning")
                    return render_template("add_car.html", role="admin", users=users, form_data=form_data)

                if not admin_actions.add_car(**form_data):
                    flash("Failed to add car.", "danger")
                    return render_template("add_car.html", role="admin", users=users, form_data=form_data)
                
                return redirect(url_for("list_cars"))
                
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)
        
        return render_template("add_car.html", role="admin", users=users)

    @app.route("/admin/cars/update/<int:car_id>", methods=["GET", "POST"])
    def update_car(car_id):
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))
        
        users = admin_actions.get_all_users()
        if not users:
                flash(ERROR_NO_USERS_FOUND, "warning")
                return redirect(url_for("list_cars"))
        
        car = helpers.get_car_by_id(car_id)
        if not car:
            flash(ERROR_CAR_NOT_FOUND, "danger")
            return redirect(url_for("list_cars"))
        
        if request.method == "POST":
            try:
                form_data = {
                    "user_id": request.form.get("user_id"),
                    "name": request.form.get("name"),
                    "model": request.form.get("model"),
                    "year": request.form.get("year"),
                    "vin": request.form.get("vin")
                }

                if not admin_actions.update_car(car_id, **form_data):
                    flash("Failed to update car.", "danger")
                    return render_template("update_car.html", role="admin", users=users, car=car)
                
                return redirect(url_for("list_cars")) 

            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)
            
        return render_template("update_car.html", role="admin", users=users, car=car)

    @app.route("/admin/services")
    def list_services():
        if not Helpers.check_admin_session():
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
                "admin/services.html", services=services
            )

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}") 
            error_message = f"An error occurred: {str(e)}"
            return render_template("error.html", error_message=error_message)

    @app.route("/admin/services/add", methods=["GET", "POST"])
    def add_service():
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))
        
        cars = admin_actions.get_all_cars()
        if not cars:
                flash(ERROR_NO_CARS_FOUND, "warning")
                return redirect(url_for("list_services"))
        
        if request.method == "POST":
            try:
                form_data = {
                    "car_id": request.form.get("car_id").strip(),
                    "mileage": request.form.get("mileage").strip(),
                    "service_type": request.form.get("service_type").strip(),
                    "service_date": request.form.get("service_date").strip(),
                    "next_service_date": request.form.get("next_service_date").strip(),
                    "cost": request.form.get("cost").strip(),
                    "notes": request.form.get("notes").strip()
                }

                form_data["car_id"] = int(form_data["car_id"])
                form_data["mileage"] = int(form_data["mileage"]) if form_data["mileage"] else None
                form_data["cost"] = float(form_data["cost"]) if form_data["cost"] else None

                if not form_data["next_service_date"]:
                    form_data["next_service_date"] = None 

                if not admin_actions.add_service(**form_data):
                    flash("Failed to add service.", "danger")
                    return render_template("add_service.html", role="admin", cars=cars, form_data=form_data)
                
                return redirect(url_for("list_services"))
                
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)
        
        return render_template("add_service.html", role="admin", cars=cars)

    @app.route("/admin/services/update/<int:service_id>", methods=["GET", "POST"])
    def update_service(service_id):
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))
        
        service = helpers.get_service_by_id(service_id)
        if not service:
            flash(ERROR_SERVICE_NOT_FOUND, "danger")
            return redirect(url_for("list_services"))
        
        if request.method == "POST":
            try:
                form_data = {
                    "car_id": request.form.get("car_id").strip(),
                    "mileage": request.form.get("mileage").strip(),
                    "service_type": request.form.get("service_type").strip(),
                    "service_date": request.form.get("service_date").strip(),
                    "next_service_date": request.form.get("next_service_date").strip(),
                    "cost": request.form.get("cost").strip(),
                    "notes": request.form.get("notes").strip()
                }

                form_data["mileage"] = int(form_data["mileage"]) if form_data["mileage"] else None
                form_data["cost"] = float(form_data["cost"]) if form_data["cost"] else None

                if not form_data["next_service_date"]:
                    form_data["next_service_date"] = None 
                
                if not admin_actions.update_service(service_id, **form_data):
                    flash("Failed to update service.", "danger")
                    return render_template("update_service.html", role="admin", service=service, form_data=form_data)
                
                return redirect(url_for("list_services"))

            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)

        return render_template("update_service.html", role="admin", service=service)

    @app.route("/admin/<entity>/delete/<int:item_id>", methods=["GET", "POST"])
    def delete_entity(entity, item_id):
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))

        if entity == "users":
            item = helpers.get_user_by_id(item_id)
            entity_name = "User"
        elif entity == "cars":
            item = helpers.get_car_by_id(item_id)
            entity_name = "Car"
        elif entity == "services":
            item = helpers.get_service_by_id(item_id)
            entity_name = "Service"
        else:
            flash(f"Invalid entity type: {entity}", "danger")
            return redirect(url_for("list_entities", entity=entity))

        if not item:
            flash(f"{entity_name} not found.", "warning")
            return redirect(url_for(f"list_{entity}"))
        
        if request.method == "POST":
            try:
                if entity == "users":
                    if not admin_actions.delete_user(item_id):
                        flash("Failed to delete user.", "danger")
                        return redirect(url_for(f"list_{entity}"))
                elif entity == "cars":
                    if not admin_actions.delete_car(item_id):
                        flash("Failed to delete car.", "danger")
                        return redirect(url_for(f"list_{entity}"))
                elif entity == "services":
                    if not admin_actions.delete_service(item_id):
                        flash("Failed to delete service.", "danger")
                        return redirect(url_for(f"list_{entity}"))

                return redirect(url_for(f"list_{entity}"))
            
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}") 
                error_message = f"An error occurred: {str(e)}"
                return render_template("error.html", error_message=error_message)

        return render_template("confirmation.html", entity=entity, item=item, entity_name=entity_name)
    
    @app.route("/admin/export/csv", methods=["GET", "POST"])
    def export_csv(export_type="users"):
        if not Helpers.check_admin_session():
            return redirect(url_for("index"))
        
        if request.method == "POST":
            export_type = request.form.get("export_type")

            downloads_folder = helpers.get_downloads_folder()
            file_name = f"{export_type}_adm.csv"
            file_path = os.path.join(downloads_folder, file_name)

            try:
                data, headers = [], []
                if export_type == "users":
                    data = admin_actions.get_all_users()
                    headers = ["ID", "Username", "Role", "Email"]
                elif export_type == "cars":
                    data = admin_actions.get_all_cars()
                    headers = ["ID", "Name", "Model", "Year", "Owner", "Service"]
                elif export_type == "services":
                    data = admin_actions.get_all_services()
                    headers = ["ID", "Car Name", "Service Type", "Service Date", "Next Service Date", "Notes"]

                if not data:
                    flash("No data found", "warning")
                    return redirect(url_for("export_csv", export_type=export_type))

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
        
        return render_template("export_csv.html", export_type=export_type)
                
        
        