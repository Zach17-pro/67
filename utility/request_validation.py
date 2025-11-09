from typing import Optional, Any
from datetime import datetime


class RequestValidation:
    ALLOWED_STATUSES = {"Open", "In Progress", "Completed", "Cancelled"}
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

    @staticmethod
    def _require_status(status: str) -> None:
        if status not in RequestValidation.ALLOWED_STATUSES:
            raise ValueError(f"status must be one of {sorted(RequestValidation.ALLOWED_STATUSES)}")

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
