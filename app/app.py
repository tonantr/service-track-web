from flask import Flask, render_template
from app.services.database_handler import DatabaseHandler

app = Flask(__name__)

db_handler = DatabaseHandler()


@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
