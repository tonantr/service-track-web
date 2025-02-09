from flask import session, redirect, url_for


def init_app(app):
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))
