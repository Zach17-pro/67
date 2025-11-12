from flask import Blueprint, jsonify, request, current_app
from control.report_controller import GetReportData
from entity.match_repository import MatchRepository
from entity.pin_request_repository import RequestRepository
from entity.shortlist_repository import ShortlistRepository
from entity.user_repository import UserRepository
from entity.request_view_repository import RequestViewRepository

report_page_api = Blueprint("report_api", __name__, url_prefix="/api/report")

def match_repo():
    db = current_app.config["DB"]
    return MatchRepository(db)

def req_repo():
    db = current_app.config["DB"]
    return RequestRepository(db)

def shortlist_repo():
    db = current_app.config["DB"]
    return ShortlistRepository(db)

def user_repo():
    db = current_app.config["DB"]
    return UserRepository(db)

def req_view_repo():
    db = current_app.config["DB"]
    return RequestViewRepository(db)

@report_page_api.get("")
def getReport():
    try:
        days = request.args.get("days", type=int)
        controller = GetReportData(match_repo(), req_repo(), shortlist_repo(), user_repo(), req_view_repo())
        results = controller.execute(days = days)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
