# entity/request.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Request:
    request_id: int
    pin_user_id: int
    title: str
    description: str
    status: str  # 'Open' | 'In Progress' | 'Completed' | 'Cancelled'
    created_at: datetime
    updated_at: datetime
    view_count: int
    shortlist_count: int
    category_id: Optional[int]
    location: str
