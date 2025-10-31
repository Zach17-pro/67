# entity/match.py
from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime

@dataclass
class Match:
    match_id: int
    request_id: int
    csr_user_id: int
    pin_user_id: int
    service_date: date
    completion_date: Optional[datetime]
    status: str  # 'Scheduled' | 'In Progress' | 'Completed' | 'Cancelled'

    # Denormalised fields (from joined tables for convenience in the app layer)
    request_title: Optional[str] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    location: Optional[str] = None
