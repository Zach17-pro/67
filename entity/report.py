from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional, Dict

@dataclass
class StatusSnapshot:
    open: int
    in_progress: int
    completed: int
    cancelled: int

@dataclass
class LocationCount:
    location: str
    count: int

@dataclass
class CategoryCount:
    category: str
    count: int

@dataclass
class ReportSummary:
    from_ts: datetime
    to_ts: datetime
    requests_created: int
    request_views: int
    request_shortlists: int
    matches_created: int
    matches_completed: int
    status_snapshot: StatusSnapshot
    avg_time_to_completion_days: Optional[float]
    by_location: List[LocationCount]
    by_category: List[CategoryCount]
    new_csrs: int
    active_csrs: int
