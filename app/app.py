from flask import Flask
import os
from app.routes.auth.auth_routes import init_app as init_auth_routes
from app.routes.admin.admin_routes import init_app as init_admin_routes
from app.routes.user.user_routes import init_app as init_user_routes
from app.routes.logout.logout_routes import init_app as init_logout_routes
from app.database.database_handler import DatabaseHandler
from app.utils.helpers import Helpers
from app.auth.login import Login

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

db_handler = DatabaseHandler()
helpers = Helpers(db_handler)
login = Login(helpers)

init_auth_routes(app, login)
init_admin_routes(app)
init_user_routes(app)
init_logout_routes(app)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=8000, debug=False)
