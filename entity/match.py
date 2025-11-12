# entity/match.py
from dataclasses import dataclass
from typing import Any, Dict, Optional
from datetime import date, datetime

from entity.pin_request import Request

@dataclass
class Match:
    match_id: int
    request_id: int
    csr_user_id: int
    pin_user_id: int
    service_date: date
    completion_date: Optional[datetime]
    request: Optional[Request] = None

    # ---------- helpers ----------
    @staticmethod
    def _row_to_match(row: Dict[str, Any]):
        return Match(
            match_id=row["match_id"],
            request_id=row["request_id"],
            csr_user_id=row["csr_user_id"],
            pin_user_id=row["pin_user_id"],
            service_date=row["service_date"],
            completion_date=row.get("completion_date"),
        )
    
    def set_request(self, request: Request) -> None:
        self.request = request