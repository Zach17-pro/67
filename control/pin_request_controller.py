# app/controllers/pin_request_controller.py
from __future__ import annotations

from typing import List, Optional
from datetime import datetime
from entity.pin_request import Request
from entity.pin_request_repository import RequestRepository
from entity.match_repository import MatchRepository


class PinRequestController:
    """
    Controller for PIN request flows (#23–#27).
    Performs lightweight validation and delegates to RequestRepository.
    Also ensures a row exists in `match` when a request becomes Completed.
    """

    ALLOWED_STATUSES = {"Open", "In Progress", "Completed", "Cancelled"}

    def __init__(self, request_repo: RequestRepository, match_repo: Optional[MatchRepository] = None):
        self.request_repo = request_repo
        self.match_repo = match_repo

    # -------- #23: Create a request --------
    def create_request(
        self,
        *,
        pin_user_id: int,
        title: str,
        description: str,
        location: str,
        category_id: Optional[int] = None,
    ) -> Request:
        self._require_positive_id(pin_user_id, "pin_user_id")
        self._require_text(title, "title")
        self._require_text(description, "description")
        self._require_text(location, "location")
        if category_id is not None:
            self._require_positive_id(category_id, "category_id")

        return self.request_repo.create_request(
            pin_user_id=pin_user_id,
            title=title.strip(),
            description=description.strip(),
            category_id=category_id,
            location=location.strip(),
        )

    # -------- #24: View my requests --------
    def list_my_requests(
        self, *, pin_user_id: int, status: Optional[str] = None, order_desc: bool = True
    ) -> List[Request]:
        self._require_positive_id(pin_user_id, "pin_user_id")
        if status is not None:
            self._require_status(status)
        return self.request_repo.list_requests_by_pin(
            pin_user_id=pin_user_id, status=status, order_desc=order_desc
        )

    # -------- #25: Update my request --------
    def update_request(
        self,
        *,
        pin_user_id: int,
        request_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category_id: Optional[int] = None,
        location: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[Request]:
        self._require_positive_id(pin_user_id, "pin_user_id")
        self._require_positive_id(request_id, "request_id")
        if title is not None:
            self._require_text(title, "title")
        if description is not None:
            self._require_text(description, "description")
        if location is not None:
            self._require_text(location, "location")
        if category_id is not None:
            self._require_positive_id(category_id, "category_id")
        if status is not None:
            self._require_status(status)

        updated = self.request_repo.update_request(
            request_id=request_id,
            pin_user_id=pin_user_id,
            title=title.strip() if isinstance(title, str) else title,
            description=description.strip() if isinstance(description, str) else description,
            category_id=category_id,
            location=location.strip() if isinstance(location, str) else location,
            status=status,
        )

        # If the request was (or is now) Completed, ensure a Completed match row exists.
        # NOTE: We use pin_user_id as a placeholder csr_user_id if none is known.
        #       Replace with the actual CSR id when you have it in your flow.
        if updated and status == "Completed" and self.match_repo is not None:
            try:
                self.match_repo.ensure_completed_match(
                    request_id=request_id,
                    pin_user_id=pin_user_id,
                    csr_user_id=pin_user_id,  # TODO: provide real CSR user id when available
                )
            except Exception:
                # Don't block the request update if match creation fails; surface via logs if desired.
                pass

        return updated

    # -------- #26: Delete my request --------
    def delete_request(self, *, pin_user_id: int, request_id: int) -> bool:
        self._require_positive_id(pin_user_id, "pin_user_id")
        self._require_positive_id(request_id, "request_id")
        deleted = self.request_repo.delete_request(request_id=request_id, pin_user_id=pin_user_id)
        return deleted is not None

    # -------- #27: Search my requests --------
    def search_my_requests(
        self,
        *,
        pin_user_id: int,
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        category_id: Optional[int] = None,
        date_from: Optional[datetime | str] = None,
        date_to: Optional[datetime | str] = None,
        order_desc: bool = True,
    ) -> List[Request]:
        self._require_positive_id(pin_user_id, "pin_user_id")
        if status is not None:
            self._require_status(status)
        if category_id is not None:
            self._require_positive_id(category_id, "category_id")

        dt_from = self._parse_dt(date_from) if date_from else None
        dt_to = self._parse_dt(date_to) if date_to else None
        self._require_dt_order(dt_from, dt_to)

        return self.request_repo.search_requests(
            pin_user_id=pin_user_id,
            keyword=(keyword.strip() if isinstance(keyword, str) and keyword.strip() else None),
            status=status,
            category_id=category_id,
            date_from=dt_from,
            date_to=dt_to,
            order_desc=order_desc,
        )

    # ----------------------
    # Validation utilities
    # ----------------------
    @staticmethod
    def _require_text(value: str, field: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} is required")

    @staticmethod
    def _require_positive_id(value: Optional[int], field: str) -> None:
        if value is None or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field} must be a positive integer")

    def _require_status(self, status: str) -> None:
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(f"status must be one of {sorted(self.ALLOWED_STATUSES)}")

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
        # final attempt: fromisoformat
        try:
            return datetime.fromisoformat(v)
        except Exception as e:
            raise ValueError("Invalid datetime format") from e

    @staticmethod
    def _require_dt_order(dt_from: Optional[datetime], dt_to: Optional[datetime]) -> None:
        if dt_from and dt_to and dt_from > dt_to:
            raise ValueError("date range is invalid: start > end")
