from flask import Flask, render_template, request, redirect, flash, url_for, session
from app.database.database_handler import DatabaseHandler
from app.utils.helpers import Helpers
from app.auth.login import Login
import os
from app.utils.constants import ERROR_USER_NOT_FOUND, ERROR_PLEASE_LOG_IN

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

db_handler = DatabaseHandler()
helpers = Helpers(db_handler)
login = Login(helpers)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if login.authenticate(username, password):
            session["username"] = username
            session["role"] = login.role
            return redirect(
                url_for(
                    "admin_dashboard" if login.role == "admin" else "user_dashboard"
                )
            )
        else:
            flash(ERROR_USER_NOT_FOUND, "error")
            return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if "username" not in session or session.get("role") != "admin":
        flash(ERROR_PLEASE_LOG_IN, "error")
        return redirect(url_for("index"))

    return render_template(
        "admin_dashboard.html", logged_in_user=session["username"], role=session["role"]
    )


@app.route("/user/dashboard")
def user_dashboard():
    if "username" not in session or session.get("role") != "user":
        flash(ERROR_PLEASE_LOG_IN, "error")
        return redirect(url_for("index"))

    return render_template(
        "user_dashboard.html", logged_in_user=session["username"], role=session["role"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
