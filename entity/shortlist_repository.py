from datetime import datetime
from entity.shortlist import Shortlist
from typing import List, Dict, Optional, Any

class ShortlistRepository:
  
    def __init__(self, db):
        self.db = db

    # -----------------------------
    # csr_save_shortlist_boundary.py
    # -----------------------------
    def save_shortlist(self, csr_id: int, request_id: int, notes: Optional[str], added_at: datetime) -> None:
        cur = self.db.cursor()
        try:
            cur.execute(
                "INSERT INTO shortlist (csr_user_id, request_id, notes, added_at) VALUES (%s, %s, %s, %s)",
                (csr_id, request_id, notes, added_at)
            )
            self.db.commit()
        finally:
            cur.close()

    # -----------------------------
    # csr_view_shortlist_boundary.py
    # -----------------------------
    def view_shortlist(self, csr_id: int, query: str) -> List[Dict[str, Any]]:
        cur = self.db.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT * FROM shortlist s
                JOIN request r ON s.request_id = r.request_id
                WHERE s.csr_user_id = %s AND (r.title LIKE %s OR r.description LIKE %s OR s.notes LIKE %s)
                ORDER BY r.created_at DESC
            """, (csr_id, f"%{query}%", f"%{query}%", f"%{query}%"))
            return cur.fetchall()
        finally:
            cur.close()