from flask import Blueprint, jsonify, request, current_app
from control.user_controller import UserController
from entity.user_repository import UserRepository

admin_api = Blueprint("admin_api", __name__, url_prefix="/api/admin")

def controller() -> UserController:
    repo = UserRepository(current_app.config["DB"])
    return UserController(repo)