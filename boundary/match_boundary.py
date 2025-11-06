# app/boundaries/match_boundary.py
from __future__ import annotations

from flask import Blueprint, jsonify, request, current_app
from dataclasses import asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, date

from entity.match_repository import MatchRepository
from entity.pin_request_repository import RequestRepository
from control.match_controller import MatchController

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

def _normalize_match(m) -> Dict[str, Any]:
    """Ensure dates are strings and keys exist as expected by the frontend."""
    d = _match_to_dict(m)
    sd = d.get("service_date")
    cd = d.get("completion_date")
    if isinstance(sd, (datetime, date)):
        d["service_date"] = sd.isoformat()
    if isinstance(cd, (datetime, date)):
        d["completion_date"] = cd.isoformat(sep=" ") if isinstance(cd, datetime) else cd.isoformat()
    d.setdefault("request_title", d.get("request_title"))
    d.setdefault("category_name", d.get("category_name"))
    d.setdefault("category_id", d.get("category_id"))
    d.setdefault("location", d.get("location"))
    return d

def _list_to_dicts(items) -> List[Dict[str, Any]]:
    return [_normalize_match(i) for i in items]

def _parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    for fmt in ("%Y-%m-%d",):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None

def _parse_dt(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    s = s.replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

# ---------- READ endpoints (keep your current behavior) ----------

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

# ---------- NEW endpoints (Part 2) ----------

# DELETE /api/pin/matches
# body: { "match_id": 123, "pin_user_id": 3 }   # pin_user_id optional (include to enforce ownership)
@match_api.delete("")
def delete_match():
    try:
        data = request.get_json(force=True) or {}
        match_id = data.get("match_id")
        pin_user_id = data.get("pin_user_id")

        if not match_id:
            return jsonify({"error": "match_id is required"}), 400

        db = current_app.config["DB"]
        repo = MatchRepository(db)
        deleted = repo.delete_match(int(match_id), int(pin_user_id) if pin_user_id is not None else None)
        if not deleted:
            return jsonify({"success": False, "error": "Match not found or not allowed"}), 404

        return jsonify({"success": True, "deleted": _normalize_match(deleted)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST /api/pin/matches/undo-complete
# body: { "request_id": 456, "pin_user_id": 3, "new_status": "Open" }  # new_status optional (default "Open")
@match_api.post("/undo-complete")
def undo_complete():
    try:
        data = request.get_json(force=True) or {}
        request_id = data.get("request_id")
        pin_user_id = data.get("pin_user_id")
        new_status = (data.get("new_status") or "Open").strip()

        if not request_id or not pin_user_id:
            return jsonify({"error": "request_id and pin_user_id are required"}), 400

        db = current_app.config["DB"]
        mrepo = MatchRepository(db)
        rrepo = RequestRepository(db)

        # 1) delete all matches for this request (owned by this PIN)
        n_deleted = mrepo.delete_by_request(int(request_id), int(pin_user_id))

        # 2) switch request away from 'Completed' so it can be edited/deleted later
        updated = rrepo.update_request(
            request_id=int(request_id),
            pin_user_id=int(pin_user_id),
            status=new_status
        )

        if not updated:
            return jsonify({
                "success": False,
                "message": "Matches removed, but request not updated (not found or not allowed).",
                "matches_deleted": n_deleted
            }), 404

        # normalize timestamps for JSON
        upd = _match_to_dict(updated)
        for k in ("created_at", "updated_at"):
            v = upd.get(k)
            if isinstance(v, (datetime, date)):
                upd[k] = v.isoformat(sep=" ") if isinstance(v, datetime) else v.isoformat()

        return jsonify({
            "success": True,
            "matches_deleted": n_deleted,
            "request": upd
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
