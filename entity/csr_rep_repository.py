from typing import List, Dict, Any, Optional
from flask import current_app
from entity.pin_request_repository import RequestRepository
from entity.match_repository import MatchRepository

class CSRRepRepository:
    def __init__(self):
        db = current_app.config["DB"]
        self.db = db
        self.request_repo = RequestRepository()
        self.match_repo = MatchRepository()

    # -----------------------------
    # csr_search_requests_boundary.py
    # -----------------------------
    def search_requests(self, query: str) -> List[Dict[str, Any]]:
        cur = self.db.cursor(dictionary=True)
        try:
            cur.execute( """
                SELECT request_id, pin_user_id, title, description, status, location
                FROM request
                WHERE status IN ('Open','In Progress') AND (title LIKE %s OR description LIKE %s)
                ORDER BY created_at DESC
            """)
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()

    # -----------------------------
    # csr_view_request_boundary.py
    # -----------------------------
    def view_request(self, request_id: int) -> Optional[Dict[str, Any]]:
        req = self.request_repo.get_request_by_id(request_id)
        return req.__dict__ if req else None

    # -----------------------------
    # csr_search_past_matches_boundary.py
    # -----------------------------
    def search_past_matches(
        self,
        service: str = "",
        start_date: str = None,
        end_date: str = None
    ) -> List[Dict[str, Any]]:
        return self.match_repo.search_past_matches(
            service_name=service,
            date_from=start_date,
            date_to=end_date
        )

    # -----------------------------
    # csr_view_past_matches_boundary.py
    # -----------------------------
    def view_past_matches(
        self,
        service: str = "",
        start_date: str = None,
        end_date: str = None
    ) -> List[Dict[str, Any]]:
        return self.match_repo.list_past_matches(
            service_name=service,
            date_from=start_date,
            date_to=end_date
        )