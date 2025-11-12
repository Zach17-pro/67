from datetime import datetime, timedelta
from entity.match_repository import MatchRepository
from entity.pin_request_repository import RequestRepository
from entity.report import LocationCount, ReportSummary, StatusSnapshot, CategoryCount
from entity.shortlist_repository import ShortlistRepository
from entity.user_repository import UserRepository
from entity.request_view_repository import RequestViewRepository


class GetReportData:
    def __init__(self, match_repo: MatchRepository, req_repo: RequestRepository
                 , shortlist_repo: ShortlistRepository, user_repo: UserRepository
                 , req_view_repo: RequestViewRepository):
        self.match_repo = match_repo
        self.request_repo = req_repo
        self.shortlist_repo = shortlist_repo
        self.user_repo = user_repo
        self.request_view_repo = req_view_repo

    def execute(self, days: int) -> ReportSummary:
        to_ts = datetime.now()
        from_ts = to_ts - timedelta(days=days)

        requests_created = self.request_repo.count_created(from_ts, to_ts)
        request_views = self.request_view_repo.count_views(from_ts, to_ts)
        request_shortlists = self.shortlist_repo.count_shortlists(from_ts, to_ts)

        matches_created = self.match_repo.count_created(from_ts, to_ts)
        matches_completed = self.match_repo.count_completed(from_ts, to_ts)
        
        snapshot = self._status_snapshot(from_ts, to_ts)

        avg_secs = self.match_repo.avg_time_to_completion(from_ts, to_ts)
        avg_days = (avg_secs / 86400.0) if avg_secs is not None else None

        by_location_rows = self.request_repo.count_by_location(from_ts, to_ts)
        by_location = [LocationCount(location=r["location"], count=r["count"])
                       for r in by_location_rows]
        

        by_category_row = self.request_repo.count_by_category(from_ts, to_ts)
        by_category = [CategoryCount(category=r["category_name"], count=r["count"])
                       for r in by_category_row]
        


        new_csrs = self.user_repo.count_new_csrs(from_ts, to_ts)
        active_csrs = self.user_repo.count_active_csrs(from_ts, to_ts)

        return ReportSummary(
            from_ts=from_ts, to_ts=to_ts,
            requests_created=requests_created,
            request_views=request_views,
            request_shortlists=request_shortlists,
            matches_created=matches_created,
            matches_completed=matches_completed,
            status_snapshot=snapshot,
            avg_time_to_completion_days=avg_days,
            by_location=by_location,
            by_category=by_category,
            new_csrs=new_csrs,
            active_csrs=active_csrs
        )
        

    def _status_snapshot(self, frm, to) -> StatusSnapshot:
        # snapshot “now”; for historical, add a history table
        rows = self.request_repo.status_snapshot(frm, to)
        lookup = {r["status"].lower(): r["count"] for r in rows}
        return StatusSnapshot(
            open=lookup.get("open", 0),
            in_progress=lookup.get("in progress", 0),
            completed=lookup.get("completed", 0),
            cancelled=lookup.get("cancelled", 0),
        )