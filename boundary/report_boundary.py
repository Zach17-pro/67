from flask import Blueprint, jsonify, request, current_app
from control.report_controller import GetReportData
from entity.report import ReportRepository

report_page_api = Blueprint("report_api", __name__, url_prefix="/api/report")

def report_repo():
    return ReportRepository()


@report_page_api.get("")
def getReport():
    try:
        days = request.args.get("days", type=int)
        controller = GetReportData(report_repo())
        results = controller.execute(days = days)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
