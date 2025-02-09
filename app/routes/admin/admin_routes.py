from flask import render_template, redirect, flash, url_for, session
from app.utils.constants import ERROR_PLEASE_LOG_IN, ERROR_NO_USERS_FOUND
from app.actions.admin_actions import AdminActions


admin_actions = AdminActions()

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
    
    @app.route("/admin/users")
    def list_users():
        if "username" not in session or session.get("role") != "admin":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return redirect(url_for("index"))
        
        try:
            users = admin_actions.list_users()

            if not users:
                flash(ERROR_NO_USERS_FOUND, "warning")
                return redirect(url_for("admin_dashboard"))
            
            return render_template("users.html", users=users)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("admin_dashboard"))
