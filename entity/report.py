from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional, Dict
from flask import current_app

# @dataclass
# class StatusSnapshot:
#     open: int
#     in_progress: int
#     completed: int
#     cancelled: int

@dataclass
class LocationCount:
    location: str
    count: int

# @dataclass
# class CategoryCount:
#     category: str
#     count: int

@dataclass
class ReportSummary:
    from_ts: datetime
    to_ts: datetime
    # requests_created: int
    # request_views: int
    # request_shortlists: int
    # matches_created: int
    # matches_completed: int
    # status_snapshot: StatusSnapshot
    # avg_time_to_completion_days: Optional[float]
    by_location: List[LocationCount]
    # by_category: List[CategoryCount]
    # new_csrs: int
    # active_csrs: int


class ReportRepository:
    
    def __init__(self):
        db = current_app.config["DB"]
        self.db = db

    def count_by_location(self, frm: datetime, to: datetime) -> List[Dict]:
        sql = """
            SELECT COALESCE(location,'Unknown') AS location, COUNT(*) AS count
            FROM request
            WHERE created_at >= %s AND created_at < %s
            GROUP BY COALESCE(location,'Unknown')
            ORDER BY count DESC
        """
        with self.db.cursor(dictionary=True) as cur:
            cur.execute(sql, (frm, to))
            return [LocationCount(**row) for row in cur.fetchall()]
        
    def get_report(self, frm: datetime, to: datetime) -> ReportSummary:
        print("TEST")
        return ReportSummary(
            from_ts=frm,
            to_ts=to,
            by_location=self.count_by_location(frm, to)
        )