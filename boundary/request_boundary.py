# app/boundaries/pin_request_boundary.py
from __future__ import annotations

from flask import Blueprint, jsonify, request, current_app
from dataclasses import asdict
from typing import Any, Dict, List

from entity.pin_request_repository import RequestRepository
from entity.match_repository import MatchRepository
from entity.request_view_repository import RequestViewRepository
from entity.service_category_repository import ServiceCategoryRepository
from control.request_controller import *

pin_req_api = Blueprint("pin_request_api", __name__, url_prefix="/api/requests")


def req_repo():
    db = current_app.config["DB"]
    return RequestRepository(db)

def match_repo():
    db = current_app.config["DB"]
    return MatchRepository(db)

def req_view_repo():
    db = current_app.config["DB"]
    return RequestViewRepository(db)

def cat_repo():
    db = current_app.config["DB"]
    return ServiceCategoryRepository(db)


# ---------- helpers ----------
def _req_to_dict(r) -> Dict[str, Any]:
    try:
        return asdict(r)  # dataclass
    except Exception:
        return r.__dict__  # fallback

def to_int_or_none(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None

def _list_to_dicts(items) -> List[Dict[str, Any]]:
    return [_req_to_dict(i) for i in items]


# ---------- Endpoints ----------
@pin_req_api.get("/<int:request_id>")
def get_request_by_id(request_id: int):
    try:
        controller = ReadRequestController(req_repo(), req_view_repo(), cat_repo())
        item = controller.read_request(request_id=request_id)
        if item is None:
            return jsonify({"error": "request not found"}), 404
        return jsonify(item.to_dict() if hasattr(item, "to_dict") else item)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pin_req_api.get("/active")
def search_active_requests():
    try:
        search = request.args.get("search", type=str)
        if not search:
            search = ""
        controller = SearchPinRequestController(req_repo(), cat_repo= cat_repo())
        items = controller.list_active_requests(search)
        return jsonify((items))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /api/requests?pin_user_id=3&status=Open
@pin_req_api.get("")
def list_my_requests():
    try:
        pin_user_id = request.args.get("pin_user_id", type=int)
        if not pin_user_id:
            return jsonify({"error": "pin_user_id is required"}), 400
        status = request.args.get("status")  # optional
        controller = ListMyPinRequestsController(req_repo(), match_repo(), cat_repo())
        items = controller.list_my_requests(pin_user_id=pin_user_id, status=status)
        return jsonify(_list_to_dicts(items))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST /api/requests
# body: { "pin_user_id": 3, "title": "...", "description": "...", "location": "...", "category_id": 2 }
@pin_req_api.post("")
def create_request():
    try:
        data = request.get_json(force=True) or {}
        required = ("pin_user_id", "title", "description", "location")
        missing = [k for k in required if not data.get(k)]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        req = CreatePinRequestController(req_repo(), match_repo()).create_request(
            pin_user_id=int(data["pin_user_id"]),
            title=data["title"],
            description=data["description"],
            location=data["location"],
            category_id=int(data["category_id"]) if data.get("category_id") else None,
        )
        return jsonify(_req_to_dict(req)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# PUT /api/requests
# body: { "pin_user_id": 3, "request_id": 10, "title": "...", "status": "Open", ... }
@pin_req_api.put("")
def update_request():
    try:
        data = request.get_json(force=True) or {}
        if not data.get("pin_user_id") or not data.get("request_id"):
            return jsonify({"error": "pin_user_id and request_id are required"}), 400
        print("CSr: ",data['csr_id'])
        updated = UpdatePinRequestController(req_repo(), match_repo(), cat_repo=cat_repo()).update_request(
            pin_user_id=int(data["pin_user_id"]),
            request_id=int(data["request_id"]),
            csr_user_id = to_int_or_none(data['csr_id']),
            title=data.get("title"),
            description=data.get("description"),
            location=data.get("location"),
            category_id=int(data["category_id"]) if data.get("category_id") else None,
            status=data.get("status"),
        )
        if not updated:
            return jsonify({"success": False, "message": "Update failed or not allowed"}), 400
        return jsonify({"success": True, "item": _req_to_dict(updated)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE /api/requests
# body: { "pin_user_id": 3, "request_id": 10 }
@pin_req_api.delete("")
def delete_request():
    try:
        data = request.get_json(force=True) or {}
        if not data.get("pin_user_id") or not data.get("request_id"):
            return jsonify({"error": "pin_user_id and request_id are required"}), 400

        ok = DeleteMyPinRequestController(req_repo(), match_repo()).delete_request(
            pin_user_id=int(data["pin_user_id"]),
            request_id=int(data["request_id"]),
        )
        return jsonify({"success": bool(ok)})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409   # conflict – in use
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /api/requests/search?pin_user_id=3&keyword=...&status=...&category_id=2&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
@pin_req_api.get("/search")
def search_my_requests():
    try:
        pin_user_id = request.args.get("pin_user_id", type=int)
        if not pin_user_id:
            return jsonify({"error": "pin_user_id is required"}), 400

        items = SearchMyPinRequestsController(req_repo(), cat_repo = cat_repo()).search_my_requests(
            pin_user_id=pin_user_id,
            keyword=request.args.get("keyword"),
            status=request.args.get("status"),
            category_id=request.args.get("category_id", type=int),
            date_from=request.args.get("date_from"),
            date_to=request.args.get("date_to"),
        )
        return jsonify(_list_to_dicts(items))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
