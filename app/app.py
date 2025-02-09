from flask import Flask, render_template, request, redirect, flash, url_for
from app.database.database_handler import DatabaseHandler
from app.utils.helpers import Helpers
from app.auth.login import Login
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

db_handler = DatabaseHandler()
helpers = Helpers(db_handler)
login = Login(helpers)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if login.authenticate(username, password):
            return redirect(
                url_for(
                    "admin_dashboard" if login.role == "admin" else "user_dashboard"
                )
            )
        else:
            flash("Login failed.", "error")
            return redirect(url_for("login_page"))

    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template(
        "admin_dashboard.html", logged_in_user=login.logged_in_user, role=login.role
    )


@app.route("/user/dashboard")
def user_dashboard():
    return render_template(
        "user_dashboard.html", logged_in_user=login.logged_in_user, role=login.role
    )


if __name__ == "__main__":
    app.run(debug=True)
