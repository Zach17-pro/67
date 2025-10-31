# entity/match_repository.py
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
        cur = self.db.cursor(dictionary=True)
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
        cur.close()
        return self._row_to_match(row) if row else None

    # ---------- list/view past matches (#29) ----------
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
        View past matches (defaults to status='Completed') with optional filters.
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
              AND m.status = 'Completed'
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

        cur = self.db.cursor(dictionary=True)
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        cur.close()
        return [self._row_to_match(r) for r in rows]

    # ---------- search past matches (#28) ----------
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
              AND m.status = 'Completed'
        """
        params: List[Any] = [pin_user_id]

        if category_id is not None:
            sql += " AND r.category_id = %s"
            params.append(category_id)

        if keyword:
            # Search in request title and description
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

        cur = self.db.cursor(dictionary=True)
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        cur.close()
        return [self._row_to_match(r) for r in rows]
