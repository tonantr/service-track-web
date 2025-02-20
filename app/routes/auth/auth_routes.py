from flask import render_template, request, redirect, flash, url_for, session
from app.utils.constants import ERROR_USER_NOT_FOUND
from app.auth.auth_service import authenticate
from app.database.database_handler import DatabaseHandler
from app.utils.helpers import Helpers


def init_app(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            db_handler = DatabaseHandler()
            helpers = Helpers(db_handler)

            if authenticate(username, password, helpers):
                return redirect(
                    url_for(
                        "admin_dashboard" if session["role"] == "admin" else "user_dashboard"
                    )
                )
            else:
                flash(ERROR_USER_NOT_FOUND, "error")
                return redirect(url_for("index"))

        return render_template("index.html")
