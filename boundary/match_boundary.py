# app/boundaries/match_boundary.py
from __future__ import annotations

from flask import Blueprint, jsonify, request, current_app
from dataclasses import asdict
from typing import Any, Dict, List

from entity.match_repository import MatchRepository
from app.controllers.match_controller import MatchController

match_api = Blueprint("match_api", __name__, url_prefix="/api/pin/matches")

def controller() -> MatchController:
    db = current_app.config["DB"]
    repo = MatchRepository(db)
    return MatchController(repo)

# ---------- helpers ----------
def _match_to_dict(m) -> Dict[str, Any]:
    try:
        return asdict(m)  # dataclass
    except Exception:
        return m.__dict__

def _list_to_dicts(items) -> List[Dict[str, Any]]:
    return [_match_to_dict(i) for i in items]

# ---------- Endpoints ----------

# GET /api/pin/matches/past?pin_user_id=3&category_id=2&service_date_from=YYYY-MM-DD&...&completion_to=YYYY-MM-DDTHH:MM
@match_api.get("/past")
def view_past_matches():
    try:
        pin_user_id = request.args.get("pin_user_id", type=int)
        if not pin_user_id:
            return jsonify({"error": "pin_user_id is required"}), 400

        items = controller().view_past_matches(
            pin_user_id=pin_user_id,
            category_id=request.args.get("category_id", type=int),
            service_date_from=request.args.get("service_date_from"),
            service_date_to=request.args.get("service_date_to"),
            completion_from=request.args.get("completion_from"),
            completion_to=request.args.get("completion_to"),
        )
        return jsonify(_list_to_dicts(items))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /api/pin/matches/search?pin_user_id=3&keyword=transport&category_id=...&service_date_from=...&completion_to=...
@match_api.get("/search")
def search_past_matches():
    try:
        pin_user_id = request.args.get("pin_user_id", type=int)
        if not pin_user_id:
            return jsonify({"error": "pin_user_id is required"}), 400

        items = controller().search_past_matches(
            pin_user_id=pin_user_id,
            keyword=request.args.get("keyword"),
            category_id=request.args.get("category_id", type=int),
            service_date_from=request.args.get("service_date_from"),
            service_date_to=request.args.get("service_date_to"),
            completion_from=request.args.get("completion_from"),
            completion_to=request.args.get("completion_to"),
        )
        return jsonify(_list_to_dicts(items))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
