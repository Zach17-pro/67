from typing import List, Dict, Any, Optional
from entity.pin_request_repository import RequestRepository
from entity.match_repository import MatchRepository

class CSRRepRepository:
    def __init__(self, db):
        self.db = db
        self.request_repo = RequestRepository(db)
        self.match_repo = MatchRepository(db)

    # -----------------------------
    # csr_search_requests_boundary.py
    # -----------------------------
    def search_requests(self, query: str) -> List[Dict[str, Any]]:
        cur = self.db.cursor(dictionary=True)
        try:
            sql = """
                SELECT request_id, pin_user_id, title, description, status, location
                FROM request
                WHERE status IN ('Open','In Progress') AND (title LIKE %s OR description LIKE %s)
                ORDER BY created_at DESC
            """
            cur.execute(sql, (f"%{query}%", f"%{query}%"))
            return [RequestRepository._row_to_request(r).__dict__ for r in cur.fetchall()]
        finally:
            cur.close()

    # -----------------------------
    # csr_view_request_boundary.py
    # -----------------------------
    def view_request(self, request_id: int) -> Optional[Dict[str, Any]]:
        req = self.request_repo.get_request_by_id(request_id)
        return req.__dict__ if req else None

    # -----------------------------
    # csr_save_shortlist_boundary.py
    # -----------------------------
    def save_shortlist(self, csr_id: int, request_id: int) -> None:
        cur = self.db.cursor()
        try:
            cur.execute(
                "INSERT IGNORE INTO csr_shortlist (csr_id, request_id) VALUES (%s, %s)",
                (csr_id, request_id)
            )
            self.db.commit()
        finally:
            cur.close()

    # -----------------------------
    # csr_search_shortlist_boundary.py
    # -----------------------------
    def search_shortlist(self, csr_id: int, query: str) -> List[Dict[str, Any]]:
        cur = self.db.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT pr.request_id, pr.title, pr.description, pr.status, pr.location
                FROM csr_shortlist cs
                JOIN request pr ON cs.request_id = pr.request_id
                WHERE cs.csr_id = %s AND (pr.title LIKE %s OR pr.description LIKE %s)
                ORDER BY pr.created_at DESC
            """, (csr_id, f"%{query}%", f"%{query}%"))
            return cur.fetchall()
        finally:
            cur.close()

    # -----------------------------
    # csr_view_shortlist_boundary.py
    # -----------------------------
    def view_shortlist(self, csr_id: int) -> List[Dict[str, Any]]:
        cur = self.db.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT pr.request_id, pr.title, pr.description, pr.status, pr.location
                FROM csr_shortlist cs
                JOIN request pr ON cs.request_id = pr.request_id
                WHERE cs.csr_id = %s
                ORDER BY pr.created_at DESC
            """, (csr_id,))
            return cur.fetchall()
        finally:
            cur.close()

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