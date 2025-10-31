from flask import Flask
import mysql.connector

app = Flask(__name__, template_folder='./template')
app.secret_key = 'secret123'

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="SixSeven"
)
app.config["DB"] = db

# Import routes after app and db are created
from admin import *

# Register boundaries
from boundary.auth_boundary import auth_api
from boundary.role_page_boundary import role_page_api
from boundary.health_boundary import health_api
from boundary.platform_manager_boundary import pm_api
# oppstoppas PIN boundary

app.register_blueprint(auth_api)
app.register_blueprint(role_page_api)
app.register_blueprint(health_api)
app.register_blueprint(pm_api)


if __name__ == '__main__':
    app.run(debug=True)
