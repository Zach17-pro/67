from flask import Blueprint, jsonify, current_app
from control.shortlist_controller import *
from entity.csr_rep_repository import CSRRepRepository
from entity.shortlist_repository import ShortlistRepository
from flask import Blueprint, jsonify, request, current_app

csr_shortlist_api = Blueprint("csr_shortlist_api", __name__, url_prefix="/api/shortlist")

def repo():
    db = current_app.config["DB"]
    return CSRRepRepository(db)

def shortRepo():
    db = current_app.config["DB"]
    return ShortlistRepository(db)

@csr_shortlist_api.get("")
def csr_view_shortlist():
    try:
        csr_id = request.args.get("csr_id", type=int)
        if not csr_id:
            return jsonify({"error": "pin_user_id is required"}), 400
        search = request.args.get("search", type=str)
        if not search:
            search = ""
        results = ViewShortlistController(shortRepo()).get_shortlist(csr_id, search)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@csr_shortlist_api.post("")
def save_shortlist():
    """
    Save PIN request to CSR's shortlist
    """
    try:
        csr_id = request.args.get("csr_id", type=int)
        if not csr_id:
            return jsonify({"error": "pin_user_id is required"}), 400
        data = request.get_json()
        request_id = data.get("request_id")
        notes = data.get("notes")
        result = SaveShortlistController(shortRepo()).add_to_shortlist(csr_id=csr_id, request_id=request_id, notes=notes)
        return jsonify({"message": "Shortlist saved"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @csr_shortlist_api.get("/search")
# def search_shortlist():
#     """
#     Search CSR's shortlist by filters: keyword, status, category_id
#     """
#     try:
#         csr_id = request.args.get("csr_id")
#         keyword = request.args.get("keyword")
#         status = request.args.get("status")
#         category_id = request.args.get("category_id", type=int)

#         db = current_app.config["DB"]
#         repo = RequestRepository(db)
#         items = repo.search_shortlist(
#             csr_id=csr_id,
#             keyword=keyword,
#             status=status,
#             category_id=category_id,
#         )

#         return jsonify([i.__dict__ for i in items])
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500