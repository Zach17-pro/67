from datetime import datetime

from flask import current_app
from entity.shortlist import Shortlist
from typing import List, Dict, Optional, Any

class ShortlistRepository:
  
    def __init__(self):
        db = current_app.config["DB"]
        self.db = db


    def save_shortlist(self, csr_id: int, request_id: int, notes: Optional[str], added_at: datetime) -> None:
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute(
                "INSERT INTO shortlist (csr_user_id, request_id, notes, added_at) VALUES (%s, %s, %s, %s)",
                (csr_id, request_id, notes, added_at)
            )
            self.db.commit()
            print("TEST")
        finally:
            cur.close()



    def get_shortlist_by_userid_and_requestid(self, csr_id: int, request_id: int):
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute(
                "SELECT * FROM shortlist WHERE csr_user_id = %s AND request_id = %s",
                (csr_id, request_id)
            )
            row = cur.fetchone()
            # With buffered=True, no additional fetchall() is needed; the driver already read all rows.
            return row
        finally:
            cur.close()


    def delete_shortlist_by_userid_and_requestid(self, csr_id: int, request_id: int) -> bool:
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute(
                "DELETE FROM shortlist WHERE csr_user_id = %s AND request_id = %s",
                (csr_id, request_id)
            )
            self.db.commit()
            return cur.rowcount > 0
        finally:
            cur.close()



    def view_shortlist(self, csr_id: int, query: str) -> List[Dict[str, Any]]:
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute("""
                SELECT * FROM shortlist s
                JOIN request r ON s.request_id = r.request_id
                WHERE s.csr_user_id = %s
                AND (r.title LIKE %s OR r.description LIKE %s OR s.notes LIKE %s)
                ORDER BY r.created_at DESC
            """, (csr_id, f"%{query}%", f"%{query}%", f"%{query}%"))
            rows = cur.fetchall()
            return rows
        finally:
            cur.close()


    # ------------------------------------
    #33 PIN view request shortlisted count
    # ------------------------------------
    def view_shortlist_count(self, request_id: int) -> int:
        cur = self.db.cursor(buffered=True)
        try:
            cur.execute("SELECT COUNT(*) FROM shortlist WHERE request_id = %s", (request_id,))
            return int(cur.fetchone()[0])
        finally:
            cur.close()


    def search_shortlist(self, csr_id: int, query: str) -> List[Dict[str, Any]]:
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            sql = """
                SELECT 
                    s.shortlist_id, s.csr_user_id, s.request_id, s.notes, s.added_at, r.title,
                    r.description, r.status, r.category_id, r.created_at
                FROM shortlist s
                JOIN request r ON s.request_id = r.request_id
                WHERE s.csr_user_id = %s
                AND (r.title LIKE %s OR r.description LIKE %s OR s.notes LIKE %s)
                ORDER BY r.created_at DESC
            """
            like = f"%{query}%"
            cur.execute(sql, (csr_id, like, like, like))
            return cur.fetchall()
        finally:
            cur.close()


    def count_shortlists(self, frm: datetime, to: datetime) -> int:
        sql = "SELECT COUNT(*) FROM shortlist WHERE added_at >= %s AND added_at < %s"
        with self.db.cursor() as cur:
            cur.execute(sql, (frm, to))
            return int(cur.fetchone()[0])
