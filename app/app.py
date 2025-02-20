from flask import Flask
import os
from app.routes.auth.auth_routes import init_app as init_auth_routes
from app.routes.admin.admin_routes import init_app as init_admin_routes
from app.routes.user.user_routes import init_app as init_user_routes
from app.routes.logout.logout_routes import init_app as init_logout_routes

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

init_auth_routes(app)
init_admin_routes(app)
init_user_routes(app)
init_logout_routes(app)
