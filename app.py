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


# Register boundaries
from boundary.auth_boundary import auth_api
from boundary.role_page_boundary import role_page_api
from boundary.health_boundary import health_api
from boundary.platform_manager_boundary import pm_api
from boundary.request_boundary import pin_req_api
from boundary.match_boundary import match_api
from boundary.shortlist_boundary import csr_shortlist_api
from boundary.admin_boundary import admin_api
from boundary.user_boundary import user_api
from boundary.report_boundary import report_page_api


app.register_blueprint(auth_api)
app.register_blueprint(role_page_api)
app.register_blueprint(health_api)
app.register_blueprint(pm_api)
app.register_blueprint(pin_req_api)  
app.register_blueprint(match_api)    
app.register_blueprint(csr_shortlist_api)
app.register_blueprint(admin_api)
app.register_blueprint(user_api)
app.register_blueprint(report_page_api)


if __name__ == '__main__':
    app.run(debug=True)
