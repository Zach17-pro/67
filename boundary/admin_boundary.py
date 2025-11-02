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
from control.user_controller import UserController
from entity.user_repository import UserRepository

admin_api = Blueprint("admin_api", __name__, url_prefix="/api/admin")

def controller() -> UserController:
    db = current_app.config["DB"]
    repo = UserRepository(db)
    return UserController(repo)

###########################
###### USER ACCOUNTS ######
###########################

#2 As a user admin, I want to create user accounts so that new users can access the system.
# CREATE - Add a new user
@admin_api.post("/users")
def create_user():
    try:
        data = request.get_json(force=True) or {}
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")
        full_name = data.get("full_name")

        if not username or not password or not role or not full_name:
            return jsonify({"error": "All fields are required"}), 400

        new_user = controller().create_user(username, password, role, full_name)
        return jsonify({"success": True, "user": new_user.to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#3 As a user admin, I want to view user accounts so that I can retrieve stored information.
# READ - List all user accounts
@admin_api.get("/users")
def get_users():
    try:
        users = controller().list_users()
        return jsonify([u.to_dict() for u in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#4 As a user admin, I want to update user accounts so that the latest information is stored.
# UPDATE - Modify an existing user
@admin_api.put("/users")
def update_user():
    try:
        data = request.get_json(force=True) or {}
        user_id = data.get("id")
        username = data.get("username")
        role = data.get("role")
        password = data.get("password")

        if not user_id or not username or not role:
            return jsonify({"error": "User ID, username, and role are required"}), 400

        controller().update_user(user_id, username, role, password)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#5 As a user admin, I want to delete user accounts so that unused or invalid accounts are removed.
# DELETE - Remove a user
@admin_api.delete("/users")
def delete_user():
    try:
        data = request.get_json(force=True) or {}
        user_id = data.get("id")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        controller().delete_user(user_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#6 As a user admin, I want to search for user accounts so that I can quickly locate them.
# SEARCH - Find users by keyword
@admin_api.get("/users/search")
def search_user():
    try:
        keyword = request.args.get("q", "").strip()
        users = controller().search_users(keyword)
        return jsonify([u.to_dict() for u in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


###########################
###### USER PROFILES ######
###########################

#7 As a user admin, I want to create user profiles so that users’ details are recorded.
@admin_api.post("/profiles")
def create_profile():
    """Create a new user profile"""
    try:
        data = request.get_json(force=True) or {}
        username = data.get("username")
        full_name = data.get("full_name")
        email = data.get("email")

        if not username or not full_name:
            return jsonify({"error": "Username and full name are required"}), 400

        new_profile = controller().create_profile(username, full_name, email)
        return jsonify({"success": True, "profile": new_profile.to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#8 As a user admin, I want to view user profiles so that I can check stored information.
@admin_api.get("/profiles")
def get_profiles():
    """View all user profiles"""
    try:
        profiles = controller().list_profiles()
        return jsonify([p.to_dict() for p in profiles])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#9 As a user admin, I want to update user profiles so that details remain current.
@admin_api.put("/profiles")
def update_profile():
    """Update existing user profile"""
    try:
        data = request.get_json(force=True) or {}
        user_id = data.get("id")
        full_name = data.get("full_name")
        email = data.get("email")

        if not user_id or not full_name:
            return jsonify({"error": "User ID and full name are required"}), 400

        controller().update_profile(user_id, full_name, email)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#10 As a user admin, I want to delete user profiles so that invalid records are removed.
@admin_api.delete("/profiles")
def delete_profile():
    """Delete a user profile"""
    try:
        data = request.get_json(force=True) or {}
        user_id = data.get("id")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        result = controller().delete_profile(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#11 As a user admin, I want to search user profiles so that I can retrieve specific information quickly.
@admin_api.get("/profiles/search")
def search_profiles():
    """Search user profiles"""
    try:
        keyword = request.args.get("q", "").strip()
        profiles = controller().search_profiles(keyword)
        return jsonify([p.to_dict() for p in profiles])
    except Exception as e:
        return jsonify({"error": str(e)}), 500