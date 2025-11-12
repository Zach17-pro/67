# app/controllers/match_controller.py
from __future__ import annotations

from typing import List, Optional
from datetime import datetime, date
from entity.match import Match
from entity.pin_request  import Request
from entity.match_repository import MatchRepository
from entity.pin_request_repository import RequestRepository
from entity.service_category_repository import ServiceCategoryRepository


class ViewPastMatchController:
    def __init__(self, match_repo: MatchRepository, req_repo: Optional[RequestRepository], cat_repo = Optional[ServiceCategoryRepository]):
        self.match_repo = match_repo
        self.req_repo = req_repo
        self.cat_repo = cat_repo
    # -------- #29: View past matches --------
    def view_past_matches(
        self,
        *,
        user_id: int,
        user_type: str,
        category_id: Optional[int] = None,
        service_date_from: Optional[date | str] = None,
        service_date_to: Optional[date | str] = None,
        completion_from: Optional[datetime | str] = None,
        completion_to: Optional[datetime | str] = None,
        order_desc: bool = True,
    ) -> List[Match]:
        _require_positive_id(user_id, user_type)
        if category_id is not None:
            _require_positive_id(category_id, "category_id")

        svc_from = _parse_date(service_date_from) if service_date_from else None
        svc_to = _parse_date(service_date_to) if service_date_to else None
        _require_date_order(svc_from, svc_to)

        comp_from = _parse_dt(completion_from) if completion_from else None
        comp_to = _parse_dt(completion_to) if completion_to else None
        _require_dt_order(comp_from, comp_to)

        matches = [Match._row_to_match(match) for match in self.match_repo.list_past_matches(
            user_id=user_id,
            user_type=user_type,
            category_id=category_id,
            service_date_from=svc_from,
            service_date_to=svc_to,
            completion_from=comp_from,
            completion_to=comp_to,
            order_desc=order_desc,
        )]

        for match in matches:
            request = Request._row_to_request(self.req_repo.get_request_by_id(match.request_id))
            request.set_service_category(self.cat_repo.get_category(request.category_id))
            match.set_request(request)
        return matches

class SearchPastMatchController:
    def __init__(self, match_repo: MatchRepository, req_repo: Optional[RequestRepository], cat_repo = Optional[ServiceCategoryRepository]):
        self.match_repo = match_repo
        self.req_repo = req_repo
        self.cat_repo = cat_repo
    # -------- #28: Search past matches --------
    def search_past_matches(
        self,
        *,
        user_id: int,
        user_type: str,
        category_id: Optional[int] = None,
        keyword: Optional[str] = None,
        service_date_from: Optional[date | str] = None,
        service_date_to: Optional[date | str] = None,
        completion_from: Optional[datetime | str] = None,
        completion_to: Optional[datetime | str] = None,
        order_desc: bool = True,
    ) -> List[Match]:
        _require_positive_id(user_id, user_type)
        if category_id is not None:
            _require_positive_id(category_id, "category_id")

        svc_from = _parse_date(service_date_from) if service_date_from else None
        svc_to = _parse_date(service_date_to) if service_date_to else None
        _require_date_order(svc_from, svc_to)

        comp_from = _parse_dt(completion_from) if completion_from else None
        comp_to = _parse_dt(completion_to) if completion_to else None
        _require_dt_order(comp_from, comp_to)

        matches = [Match._row_to_match(match) for match in self.match_repo.search_past_matches(
            user_id=user_id,
            user_type=user_type,
            category_id=category_id,
            keyword=(keyword.strip() if isinstance(keyword, str) and keyword.strip() else None),
            service_date_from=svc_from,
            service_date_to=svc_to,
            completion_from=comp_from,
            completion_to=comp_to,
            order_desc=order_desc,
        )]

        for match in matches:
            request = Request._row_to_request(self.req_repo.get_request_by_id(match.request_id))
            request.set_service_category(self.cat_repo.get_category(request.category_id))
            match.set_request(request)

        return matches

# ----------------------
# Validation utilities
# ----------------------
@staticmethod
def _require_positive_id(value: Optional[int], field: str) -> None:
    if value is None or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field} must be a positive integer")

@staticmethod
def _parse_dt(v: datetime | str) -> datetime:
    if isinstance(v, datetime):
        return v
    v = v.replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(v)
    except Exception as e:
        raise ValueError("Invalid datetime format") from e

@staticmethod
def _parse_date(v: date | str) -> date:
    if isinstance(v, date) and not isinstance(v, datetime):
        return v
    if isinstance(v, datetime):
        return v.date()
    try:
        return date.fromisoformat(v)
    except ValueError as e:
        raise ValueError("Invalid date format (expected YYYY-MM-DD)") from e

@staticmethod
def _require_dt_order(dt_from: Optional[datetime], dt_to: Optional[datetime]) -> None:
    if dt_from and dt_to and dt_from > dt_to:
        raise ValueError("date range is invalid: start > end")

@staticmethod
def _require_date_order(d_from: Optional[date], d_to: Optional[date]) -> None:
    if d_from and d_to and d_from > d_to:
        raise ValueError("date range is invalid: start > end")
