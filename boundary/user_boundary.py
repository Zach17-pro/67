# app/boundaries/admin_boundary.py
# User Stories (User Accounts)
#2 As a user admin, I want to create user accounts so that new users can access the system.
#3 As a user admin, I want to view user accounts so that I can retrieve stored information.
#4 As a user admin, I want to update user accounts so that the latest information is stored.
#5 As a user admin, I want to delete user accounts so that unused or invalid accounts are removed.
#6 As a user admin, I want to search for user accounts so that I can quickly locate them.

# User Stories (User Profiles)
#7 As a user admin, I want to create user profiles so that users’ details are recorded.
#8 As a user admin, I want to view user profiles so that I can check stored information.
#9 As a user admin, I want to update user profiles so that details remain current.
#10 As a user admin, I want to delete user profiles so that invalid records are removed.
#11 As a user admin, I want to search user profiles so that I can retrieve specific information quickly.

from flask import Blueprint, jsonify, request, current_app
from app import db
from control.user_controller import (
    UserViewCSRController
)

from entity.user_repository import UserRepository

user_api = Blueprint("user_api", __name__, url_prefix="/api/user")

def repo() -> UserRepository:
    db = current_app.config["DB"]
    return UserRepository(db)

#3 As a user admin, I want to view user accounts so that I can retrieve stored information.
# READ - List all user accounts
@user_api.get("/csr")
def list_users():
    try:
        ctrl = UserViewCSRController(repo())
        users = ctrl.list_csr()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500