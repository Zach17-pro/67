from datetime import datetime, timedelta
from entity.match_repository import MatchRepository
from entity.pin_request_repository import RequestRepository
from entity.report import ReportSummary, ReportRepository


class GetReportData:
    def __init__(self, report_repo: ReportRepository):
        self.report_repo = report_repo
        
    def execute(self, days: int) -> ReportSummary:
        try:
            to_ts = datetime.now()
            from_ts = to_ts - timedelta(days=days)
            
            reportSummary = self.report_repo.get_report(from_ts, to_ts)

            return reportSummary
        except Exception as e:
            print(e)
        