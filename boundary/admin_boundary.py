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
    UserAdminCreateUserAccountController,
    UserAdminViewUserAccountController,
    UserAdminEditUserAccountController,
    UserAdminDeleteUserAccountController,
    UserAdminSearchUserAccountController,
    UserAdminCreateUserProfileController,
    UserAdminViewUserProfileController,
    UserAdminEditUserProfileController,
    UserAdminDeleteUserProfileController,
    UserAdminSearchUserProfileController
)

from entity.user_repository import UserRepository

admin_api = Blueprint("admin_api", __name__, url_prefix="/api/admin")

def repo() -> UserRepository:
    db = current_app.config["DB"]
    return UserRepository(db)

###########################
###### USER ACCOUNTS ######
###########################

#2 As a user admin, I want to create user accounts so that new users can access the system.
# CREATE - Add a new user
@admin_api.post("")
def create_user():
    try:
        data = request.get_json(force=True) or {}
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")
        # full_name = data.get("full_name")

        if not all([username, password, role]):
            return jsonify({"error": "All fields are required"}), 400

        ctrl = UserAdminCreateUserAccountController(repo())
        new_user = ctrl.create_user(username, password, role)
        return jsonify({"success": True, "user": new_user}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#3 As a user admin, I want to view user accounts so that I can retrieve stored information.
# READ - List all user accounts
@admin_api.get("")
def list_users():
    try:
        ctrl = UserAdminViewUserAccountController(repo())
        users = ctrl.list_users()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#4 As a user admin, I want to update user accounts so that the latest information is stored.
# UPDATE - Modify an existing user
@admin_api.put("")
def update_user():
    try:
        data = request.get_json(force=True) or {}
        user_id = data.get("id")
        username = data.get("username")
        role = data.get("role")
        password = data.get("password")

        if not user_id or not username or not role:
            return jsonify({"error": "User ID, username, and role are required"}), 400

        ctrl = UserAdminEditUserAccountController(repo())
        ctrl.update_user(user_id, username, role, password)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#5 As a user admin, I want to delete user accounts so that unused or invalid accounts are removed.
# DELETE - Remove a user
@admin_api.delete("")
def delete_user():
    try:
        data = request.get_json(force=True) or {}
        user_id = data.get("id")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        ctrl = UserAdminDeleteUserAccountController(repo())
        result = ctrl.delete_user(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#6 As a user admin, I want to search for user accounts so that I can quickly locate them.
# SEARCH - Find users by keyword
# @admin_api.get("")
# def search_users():
#     try:
#         keyword = request.args.get("q", "").strip()
#         ctrl = UserAdminSearchUserAccountController(repo())
#         users = ctrl.search_users(keyword)
#         return jsonify(users)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


###########################
###### USER PROFILES ######
###########################

#7 As a user admin, I want to create user profiles so that users’ details are recorded.
@admin_api.post("/profile")
def create_profile():
    try:
        data = request.get_json(force=True) or {}
        username = data.get("username")
        full_name = data.get("full_name")
        email = data.get("email")

        if not username or not full_name:
            return jsonify({"error": "Username and Full Name are required"}), 400

        ctrl = UserAdminCreateUserProfileController(repo())
        new_profile = ctrl.create_profile(username, full_name, email)
        return jsonify({"success": True, "profile": new_profile}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#8 As a user admin, I want to view user profiles so that I can check stored information.
@admin_api.get("/profile")
def list_profiles():
    try:
        ctrl = UserAdminViewUserProfileController(repo())
        profiles = ctrl.list_profiles()
        return jsonify(profiles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#9 As a user admin, I want to update user profiles so that details remain current.
@admin_api.put("/profile")
def update_profile():
    try:
        data = request.get_json(force=True) or {}
        user_id = data.get("id")
        full_name = data.get("full_name")
        email = data.get("email")

        if not user_id or not full_name:
            return jsonify({"error": "User ID and full name are required"}), 400

        ctrl = UserAdminEditUserProfileController(repo())
        ctrl.update_profile(user_id, full_name, email)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#10 As a user admin, I want to delete user profiles so that invalid records are removed.
@admin_api.delete("/profile")
def delete_profile():
    try:
        data = request.get_json(force=True) or {}
        user_id = data.get("id")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        ctrl = UserAdminDeleteUserProfileController(repo())
        result = ctrl.delete_profile(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#11 As a user admin, I want to search user profiles so that I can retrieve specific information quickly.
# @admin_api.get("/profile")
# def search_profiles():
#     try:
#         keyword = request.args.get("q", "").strip()
#         ctrl = UserAdminSearchUserProfileController(repo())
#         profiles = ctrl.search_profiles(keyword)
#         return jsonify(profiles)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500