# app/boundaries/platform_manager_boundary.py
from flask import Blueprint, jsonify, request, current_app
from control.service_category_controller import ServiceCategoryController
from entity.service_category_repository import ServiceCategoryRepository

pm_api = Blueprint("platform_manager_api", __name__, url_prefix="/api/platform_manager")

def controller() -> ServiceCategoryController:
    db = current_app.config["DB"]
    repo = ServiceCategoryRepository(db)
    return ServiceCategoryController(repo)

@pm_api.get("")
def pm_read_categories():
    try:
        categories = controller().read_categories()
        return jsonify(categories)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pm_api.post("")
def pm_create_category():
    try:
        data = request.get_json(force=True) or {}
        name = data.get("category_name")
        if not name:
            return jsonify({"error": "Category name is required"}), 400
        new_id = controller().create_category(name=name)
        return jsonify({"success": True, "id": new_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pm_api.put("")
def pm_update_category():
    try:
        data = request.get_json(force=True) or {}
        category_id = data.get("id")
        name = data.get("category_name")
        if not category_id or not name:
            return jsonify({"error": "Category ID and name are required"}), 400
        controller().update_category(category_id=int(category_id), name=name)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pm_api.delete("")
def pm_delete_category():
    try:
        data = request.get_json(force=True) or {}
        category_id = data.get("id")
        if not category_id:
            return jsonify({"error": "Category ID is required"}), 400
        controller().delete_category(category_id=int(category_id))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
