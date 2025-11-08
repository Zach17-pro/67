from flask import Blueprint, jsonify, current_app
from control.csr_rep_controller import CSRRepController
from entity.csr_rep_repository import CSRRepRepository

csr_view_shortlist_api = Blueprint("csr_view_shortlist_api", __name__, url_prefix="/api/csr_rep")

def controller() -> CSRRepController:
    db = current_app.config["DB"]
    repo = CSRRepRepository(db)
    return CSRRepController(repo)

@csr_view_shortlist_api.get("/view_shortlist/<int:rep_id>")
def csr_view_shortlist(rep_id):
    try:
        results = controller().view_shortlist(rep_id)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500