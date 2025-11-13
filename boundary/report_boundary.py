from flask import Blueprint, jsonify, request, current_app
from control.report_controller import GetReportData
from entity.match_repository import MatchRepository
from entity.pin_request_repository import RequestRepository
from entity.shortlist_repository import ShortlistRepository
from entity.user_repository import UserRepository
from entity.request_view_repository import RequestViewRepository

report_page_api = Blueprint("report_api", __name__, url_prefix="/api/report")

def match_repo():
    return MatchRepository()

def req_repo():
    return RequestRepository()

def shortlist_repo():
    return ShortlistRepository()

def user_repo():
    return UserRepository()

def req_view_repo():
    return RequestViewRepository()

@report_page_api.get("")
def getReport():
    try:
        days = request.args.get("days", type=int)
        controller = GetReportData(match_repo(), req_repo(), shortlist_repo(), user_repo(), req_view_repo())
        results = controller.execute(days = days)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
