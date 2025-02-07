from flask import Flask, render_template
from app.services.database_handler import DatabaseHandler

app = Flask(__name__)

db_handler = DatabaseHandler()

@app.route('/')
def index():
    try:
        db_handler.connect()
        query = "select * from cars"
        cars = db_handler.fetchall(query)
        return render_template('index.html', cars=cars)
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)


        