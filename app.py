from flask import Flask
import mysql.connector

app = Flask(__name__, template_folder='../htmls')
app.secret_key = 'secret123'

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="SixSeven"
)

# Import routes after app and db are created
from login import *
from admin import *

if __name__ == '__main__':
    app.run(debug=True)
