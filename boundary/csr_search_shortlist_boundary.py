from flask import Blueprint, jsonify, request, current_app
from control.csr_rep_controller import CSRRepController
from entity.csr_rep_repository import CSRRepRepository

csr_search_shortlist_api = Blueprint("csr_search_shortlist_api", __name__, url_prefix="/api/csr_rep")

def controller() -> CSRRepController:
    db = current_app.config["DB"]
    repo = CSRRepRepository(db)
    return CSRRepController(repo)

@csr_search_shortlist_api.get("/search_shortlist")
def csr_search_shortlist():
    try:
        rep_id = request.args.get("rep_id")
        keyword = request.args.get("keyword", "")
        if not rep_id:
            return jsonify({"error": "Rep ID is required"}), 400

        results = controller().search_shortlist(int(rep_id), keyword)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500