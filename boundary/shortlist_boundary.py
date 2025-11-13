from control.shortlist_controller import *
from flask import Blueprint, jsonify, request, current_app

csr_shortlist_api = Blueprint("csr_shortlist_api", __name__, url_prefix="/api/shortlist")

@csr_shortlist_api.get("")
def csr_view_shortlist():
    try:
        csr_id = request.args.get("csr_id", type=int)
        if not csr_id:
            return jsonify({"error": "csr_id is required"}), 400
        search = request.args.get("search", type=str)
        if not search:
            search = ""
        results = ViewShortlistController().get_shortlist(csr_id, search)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@csr_shortlist_api.post("")
def save_shortlist():
    try:
        data = request.get_json() or {}
        csr_id = data.get("pin_user_id")
        if not csr_id:
            return jsonify({"error": "pin_user_id is required"}), 400

        request_id = data.get("request_id")
        notes = data.get("notes")
        results = SaveShortlistController().toggle_shortlist(csr_id=csr_id, request_id=request_id, notes=notes)
        return jsonify({"message": "Shortlist saved"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@csr_shortlist_api.get("/search")
def search_shortlist():
    try:
        csr_id = request.args.get("csr_id", type=int)
        if not csr_id:
            return jsonify({"error": "csr_id is required"}), 400
        search = request.args.get("search", type=str)
        if not search:
            search = ""
        search = request.args.get("search", "")
        results = SearchShortlistController().search_shortlist(csr_id, search)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500