# app/entity/match_repository.py
from __future__ import annotations

from typing import List, Optional, Any, Dict
from datetime import date, datetime
from entity.match import Match


class MatchRepository:
    """
    Repository for PIN past matches and related queries.
    Joins `match` -> `request` -> `service_category` to support service/date filters.
    """

    def __init__(self, db):
        self.db = db

    # ---------- helpers ----------
    @staticmethod
    def _row_to_match(row: Dict[str, Any]) -> Match:
        return Match(
            match_id=row["match_id"],
            request_id=row["request_id"],
            csr_user_id=row["csr_user_id"],
            pin_user_id=row["pin_user_id"],
            service_date=row["service_date"],
            completion_date=row.get("completion_date"),
            status=row["status"],
            request_title=row.get("request_title"),
            category_id=row.get("category_id"),
            category_name=row.get("category_name"),
            location=row.get("location"),
        )

    # ---------- fetch one ----------
    def get_by_id(self, match_id: int, pin_user_id: Optional[int] = None) -> Optional[Match]:
        """
        Fetch a single match. If pin_user_id is provided, enforce ownership.
        """
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            base_sql = """
                SELECT
                    m.match_id, m.request_id, m.csr_user_id, m.pin_user_id,
                    m.service_date, m.completion_date, m.status,
                    r.title AS request_title, r.category_id, r.location,
                    sc.category_name
                FROM `match` m
                JOIN request r ON r.request_id = m.request_id
                LEFT JOIN service_category sc ON sc.category_id = r.category_id
                WHERE m.match_id = %s
            """
            params: List[Any] = [match_id]
            if pin_user_id is not None:
                base_sql += " AND m.pin_user_id = %s"
                params.append(pin_user_id)

            cur.execute(base_sql, tuple(params))
            row = cur.fetchone()
            return self._row_to_match(row) if row else None
        finally:
            cur.close()

    # ---------- list/view past matches ----------
    def list_past_matches(
        self,
        pin_user_id: int,
        *,
        category_id: Optional[int] = None,
        service_date_from: Optional[date] = None,
        service_date_to: Optional[date] = None,
        completion_from: Optional[datetime] = None,
        completion_to: Optional[datetime] = None,
        order_desc: bool = True,
    ) -> List[Match]:
        """
        View past matches (defaults to completed) with optional filters.
        Uses a tolerant status check to handle casing/whitespace changes.
        """
        sql = """
            SELECT
                m.match_id, m.request_id, m.csr_user_id, m.pin_user_id,
                m.service_date, m.completion_date, m.status,
                r.title AS request_title, r.category_id, r.location,
                sc.category_name
            FROM `match` m
            JOIN request r ON r.request_id = m.request_id
            LEFT JOIN service_category sc ON sc.category_id = r.category_id
            WHERE m.pin_user_id = %s
              AND TRIM(LOWER(m.status)) IN ('completed','complete')
              -- AND m.completion_date IS NOT NULL   -- uncomment if you require a timestamp
        """
        params: List[Any] = [pin_user_id]

        if category_id is not None:
            sql += " AND r.category_id = %s"
            params.append(category_id)

        if service_date_from:
            sql += " AND m.service_date >= %s"
            params.append(service_date_from)

        if service_date_to:
            sql += " AND m.service_date <= %s"
            params.append(service_date_to)

        if completion_from:
            sql += " AND m.completion_date >= %s"
            params.append(completion_from)

        if completion_to:
            sql += " AND m.completion_date <= %s"
            params.append(completion_to)

        sql += " ORDER BY m.completion_date " + ("DESC" if order_desc else "ASC")

        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            return [self._row_to_match(r) for r in rows]
        finally:
            cur.close()

    # ---------- search past matches ----------
    def search_past_matches(
        self,
        pin_user_id: int,
        *,
        category_id: Optional[int] = None,          # filter by service category
        keyword: Optional[str] = None,              # matches request.title/description
        service_date_from: Optional[date] = None,
        service_date_to: Optional[date] = None,
        completion_from: Optional[datetime] = None,
        completion_to: Optional[datetime] = None,
        order_desc: bool = True,
    ) -> List[Match]:
        """
        Search past matches (Completed) by service and date period; optional keyword on request.
        """
        sql = """
            SELECT
                m.match_id, m.request_id, m.csr_user_id, m.pin_user_id,
                m.service_date, m.completion_date, m.status,
                r.title AS request_title, r.category_id, r.location,
                sc.category_name
            FROM `match` m
            JOIN request r ON r.request_id = m.request_id
            LEFT JOIN service_category sc ON sc.category_id = r.category_id
            WHERE m.pin_user_id = %s
              AND TRIM(LOWER(m.status)) IN ('completed','complete')
              -- AND m.completion_date IS NOT NULL   -- optional
        """
        params: List[Any] = [pin_user_id]

        if category_id is not None:
            sql += " AND r.category_id = %s"
            params.append(category_id)

        if keyword:
            sql += " AND (r.title LIKE %s OR r.description LIKE %s)"
            like = f"%{keyword}%"
            params.extend([like, like])

        if service_date_from:
            sql += " AND m.service_date >= %s"
            params.append(service_date_from)

        if service_date_to:
            sql += " AND m.service_date <= %s"
            params.append(service_date_to)

        if completion_from:
            sql += " AND m.completion_date >= %s"
            params.append(completion_from)

        if completion_to:
            sql += " AND m.completion_date <= %s"
            params.append(completion_to)

        sql += " ORDER BY m.completion_date " + ("DESC" if order_desc else "ASC")

        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            return [self._row_to_match(r) for r in rows]
        finally:
            cur.close()

    # ---------- NEW: undo a completion (re-open request and delete the match) ----------
    def undo_complete(self, match_id: int, pin_user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Atomically:
          1) Fetch the match (optionally enforcing ownership),
          2) Set the corresponding request back to 'In Progress',
          3) Delete the match row.

        Returns a summary dict or None if match not found/owned.
        """
        m = self.get_by_id(match_id, pin_user_id)
        if not m:
            return None

        cur = self.db.cursor()
        try:
            # Begin a transaction
            self.db.start_transaction()

            # Re-open the request owned by the same PIN
            cur.execute(
                "UPDATE request SET status = 'In Progress' WHERE request_id = %s AND pin_user_id = %s",
                (m.request_id, m.pin_user_id),
            )
            req_updated = cur.rowcount or 0

            # Delete the match
            sql = "DELETE FROM `match` WHERE match_id = %s"
            params: List[Any] = [match_id]
            if pin_user_id is not None:
                sql += " AND pin_user_id = %s"
                params.append(pin_user_id)

            cur.execute(sql, tuple(params))
            match_deleted = cur.rowcount or 0

            self.db.commit()
            return {
                "success": True,
                "request_id": m.request_id,
                "pin_user_id": m.pin_user_id,
                "request_updated": bool(req_updated),
                "match_deleted": bool(match_deleted),
            }
        except Exception:
            self.db.rollback()
            raise
        finally:
            cur.close()

    # ---------- delete a single match ----------
    def delete_match(self, match_id: int, pin_user_id: Optional[int] = None) -> Optional[Match]:
        """
        Delete one match. If pin_user_id is provided, enforce ownership.
        Returns the deleted Match (pre-delete snapshot) or None.
        """
        existing = self.get_by_id(match_id, pin_user_id)
        if not existing:
            return None

        cur = self.db.cursor()
        try:
            sql = "DELETE FROM `match` WHERE match_id = %s"
            params: List[Any] = [match_id]
            if pin_user_id is not None:
                sql += " AND pin_user_id = %s"
                params.append(pin_user_id)

            cur.execute(sql, tuple(params))
            self.db.commit()
            return existing
        finally:
            cur.close()

    # ---------- delete all matches for a request ----------
    def delete_by_request(self, request_id: int, pin_user_id: Optional[int] = None) -> int:
        """
        Delete all matches for a request.
        Returns the number of deleted rows.
        """
        cur = self.db.cursor()
        try:
            sql = "DELETE FROM `match` WHERE request_id = %s"
            params: List[Any] = [request_id]
            if pin_user_id is not None:
                sql += " AND pin_user_id = %s"
                params.append(pin_user_id)

            cur.execute(sql, tuple(params))
            affected = cur.rowcount or 0
            self.db.commit()
            return affected
        finally:
            cur.close()

    # ---------- OPTIONAL: delete matches by category (bulk cleanup helper) ----------
    def delete_by_category(self, category_id: int, pin_user_id: Optional[int] = None) -> int:
        """
        Delete all matches whose requests are in a given category.
        Useful before deleting a category (you still need to handle requests afterwards).
        Returns number of deleted rows.
        """
        cur = self.db.cursor()
        try:
            sql = """
                DELETE m FROM `match` m
                JOIN request r ON r.request_id = m.request_id
                WHERE r.category_id = %s
            """
            params: List[Any] = [category_id]
            if pin_user_id is not None:
                sql += " AND m.pin_user_id = %s"
                params.append(pin_user_id)

            cur.execute(sql, tuple(params))
            n = cur.rowcount or 0
            self.db.commit()
            return n
        finally:
            cur.close()
