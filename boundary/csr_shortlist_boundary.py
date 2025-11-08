from flask import Blueprint, jsonify, request, current_app
from entity.pin_request_repository import RequestRepository

csr_shortlist_api = Blueprint(
    "csr_shortlist_api",
    __name__,
    url_prefix="/api/csr/shortlist",
)

@csr_shortlist_api.post("/save")
def save_shortlist():
    """
    Save PIN request to CSR's shortlist
    """
    try:
        data = request.get_json()
        request_id = data.get("request_id")
        csr_id = data.get("csr_id")  # CSR identifier

        db = current_app.config["DB"]
        repo = RequestRepository(db)
        repo.save_to_shortlist(csr_id=csr_id, request_id=request_id)

        return jsonify({"message": "Shortlist saved"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@csr_shortlist_api.get("/search")
def search_shortlist():
    """
    Search CSR's shortlist by filters: keyword, status, category_id
    """
    try:
        csr_id = request.args.get("csr_id")
        keyword = request.args.get("keyword")
        status = request.args.get("status")
        category_id = request.args.get("category_id", type=int)

        db = current_app.config["DB"]
        repo = RequestRepository(db)
        items = repo.search_shortlist(
            csr_id=csr_id,
            keyword=keyword,
            status=status,
            category_id=category_id,
        )

        return jsonify([i.__dict__ for i in items])
    except Exception as e:
        return jsonify({"error": str(e)}), 500