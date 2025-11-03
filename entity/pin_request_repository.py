##23
# As a PIN, I want to create a request so that I can seek assistance.
#24
# As a PIN, I want to view my requests so that I can see what I have submitted.
#25
# As a PIN, I want to update my requests so that I can keep them accurate.
#26
# As a PIN, I want to delete my requests so that outdated ones are removed.
#27
# As a PIN, I want to search for my requests so that I can retrieve them quickly.
#28
# As a PIN, I want to search for past matches by services, date period so that I can find past services provided to me.
#29
# As a PIN, I want to view past matches by services, date period so that I can reference completed services.

from typing import List, Optional, Any, Dict
from datetime import datetime
from entity.pin_request import Request
from entity.match_repository import MatchRepository


class RequestRepository:
    """
    Entity-focused repository for PIN request flows.
    Covers user stories:
      #23 create, #24 view mine, #25 update, #26 delete,
      #27 search mine, #28 search past matches, #29 view past matches
    """
    def __init__(self, db):
        self.db = db

    # ---------- helpers ----------
    @staticmethod
    def _row_to_request(row: Dict[str, Any]) -> Request:
        return Request(
            request_id=row["request_id"],
            pin_user_id=row["pin_user_id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            view_count=row["view_count"],
            shortlist_count=row["shortlist_count"],
            category_id=row.get("category_id"),
            location=row["location"],
        )

    # ---------- #23: Create a request ----------
    def create_request(
        self,
        pin_user_id: int,
        title: str,
        description: str,
        category_id: Optional[int],
        location: str,
    ) -> Request:
        """
        Inserts a new request with default status='Open'.
        """
        cur = self.db.cursor()
        cur.execute(
            """
            INSERT INTO request
                (pin_user_id, title, description, status, category_id, location)
            VALUES
                (%s, %s, %s, 'Open', %s, %s)
            """,
            (pin_user_id, title, description, category_id, location),
        )
        new_id = cur.lastrowid
        self.db.commit()
        cur.close()
        # Return full row
        return self.get_request_by_id(new_id)

    # ---------- utility: get by id (scoped or not) ----------
    def get_request_by_id(self, request_id: int, pin_user_id: Optional[int] = None) -> Optional[Request]:
        """
        Fetch a single request. If pin_user_id is provided, enforce ownership.
        """
        cur = self.db.cursor(dictionary=True)
        if pin_user_id is None:
            cur.execute(
                """
                SELECT request_id, pin_user_id, title, description, status,
                       created_at, updated_at, view_count, shortlist_count,
                       category_id, location
                FROM request
                WHERE request_id = %s
                """,
                (request_id,),
            )
        else:
            cur.execute(
                """
                SELECT request_id, pin_user_id, title, description, status,
                       created_at, updated_at, view_count, shortlist_count,
                       category_id, location
                FROM request
                WHERE request_id = %s AND pin_user_id = %s
                """,
                (request_id, pin_user_id),
            )
        row = cur.fetchone()
        cur.close()
        return self._row_to_request(row) if row else None

    # ---------- #24: View my requests ----------
    def list_requests_by_pin(
        self,
        pin_user_id: int,
        status: Optional[str] = None,
        order_desc: bool = True,
    ) -> List[Request]:
        """
        Returns all requests for a PIN (optionally filtered by status).
        """
        params: List[Any] = [pin_user_id]
        sql = """
            SELECT request_id, pin_user_id, title, description, status,
                   created_at, updated_at, view_count, shortlist_count,
                   category_id, location
            FROM request
            WHERE pin_user_id = %s
        """
        if status:
            sql += " AND status = %s"
            params.append(status)
        sql += " ORDER BY created_at " + ("DESC" if order_desc else "ASC")

        cur = self.db.cursor(dictionary=True)
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        cur.close()
        return [self._row_to_request(r) for r in rows]

    # ---------- #25: Update my request ----------
    def update_request(
        self,
        request_id: int,
        pin_user_id: int,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category_id: Optional[int] = None,
        location: Optional[str] = None,
        status: Optional[str] = None,  # allow status change if needed
    ) -> Optional[Request]:
        """
        Updates allowed fields for a request owned by the PIN.
        Returns the updated Request or None if not found/owned.
        """
        # Build dynamic update
        fields = []
        params: List[Any] = []
        if title is not None:
            fields.append("title = %s")
            params.append(title)
        if description is not None:
            fields.append("description = %s")
            params.append(description)
        if category_id is not None:
            fields.append("category_id = %s")
            params.append(category_id)
        if location is not None:
            fields.append("location = %s")
            params.append(location)
        if status is not None:
            # validate to table enum externally if needed
            fields.append("status = %s")
            params.append(status)

        if not fields:
            return self.get_request_by_id(request_id, pin_user_id)

        params.extend([request_id, pin_user_id])

        cur = self.db.cursor()
        cur.execute(
            f"""
            UPDATE request
            SET {", ".join(fields)}
            WHERE request_id = %s AND pin_user_id = %s
            """,
            tuple(params),
        )
        self.db.commit()
        cur.close()

        return self.get_request_by_id(request_id, pin_user_id)

    # ---------- #26: Delete my request ----------
    def delete_request(self, request_id: int, pin_user_id: int) -> Optional[Request]:
        """
        Deletes a request owned by the PIN.
        Returns a minimal Request with request_id if deleted, else None.
        """
        existing = self.get_request_by_id(request_id, pin_user_id)
        if not existing:
            return None

        cur = self.db.cursor()
        cur.execute(
            "DELETE FROM request WHERE request_id = %s AND pin_user_id = %s",
            (request_id, pin_user_id),
        )
        self.db.commit()
        cur.close()

        # mirror your category delete return style
        return Request(
            request_id=request_id,
            pin_user_id=pin_user_id,
            title=existing.title,
            description=existing.description,
            status=existing.status,
            created_at=existing.created_at,
            updated_at=existing.updated_at,
            view_count=existing.view_count,
            shortlist_count=existing.shortlist_count,
            category_id=existing.category_id,
            location=existing.location,
        )

    # ---------- #27: Search my requests ----------
    def search_requests(
        self,
        pin_user_id: int,
        *,
        keyword: Optional[str] = None,       # matches title/description
        status: Optional[str] = None,
        category_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        order_desc: bool = True,
    ) -> List[Request]:
        """
        Search a PIN's requests using common filters.
        """
        sql = """
            SELECT request_id, pin_user_id, title, description, status,
                   created_at, updated_at, view_count, shortlist_count,
                   category_id, location
            FROM request
            WHERE pin_user_id = %s
        """
        params: List[Any] = [pin_user_id]

        if keyword:
            sql += " AND (title LIKE %s OR description LIKE %s)"
            like = f"%{keyword}%"
            params.extend([like, like])

        if status:
            sql += " AND status = %s"
            params.append(status)

        if category_id is not None:
            sql += " AND category_id = %s"
            params.append(category_id)

        if date_from:
            sql += " AND created_at >= %s"
            params.append(date_from)

        if date_to:
            sql += " AND created_at <= %s"
            params.append(date_to)

        sql += " ORDER BY created_at " + ("DESC" if order_desc else "ASC")

        cur = self.db.cursor(dictionary=True)
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        cur.close()
        return [self._row_to_request(r) for r in rows]

        # ---------- #28: Search past matches (via match table) ----------
    def search_past_matches(
        self,
        pin_user_id: int,
        *,
        category_id: int | None = None,
        keyword: str | None = None,
        service_date_from=None,
        service_date_to=None,
        completion_from=None,
        completion_to=None,
        order_desc: bool = True,
    ):
        return MatchRepository(self.db).search_past_matches(
            pin_user_id=pin_user_id,
            category_id=category_id,
            keyword=keyword,
            service_date_from=service_date_from,
            service_date_to=service_date_to,
            completion_from=completion_from,
            completion_to=completion_to,
            order_desc=order_desc,
        )

    # ---------- #29: View past matches (via match table) ----------
    def view_past_matches(
        self,
        pin_user_id: int,
        *,
        category_id: int | None = None,
        service_date_from=None,
        service_date_to=None,
        completion_from=None,
        completion_to=None,
        order_desc: bool = True,
    ):
        return MatchRepository(self.db).list_past_matches(
            pin_user_id=pin_user_id,
            category_id=category_id,
            service_date_from=service_date_from,
            service_date_to=service_date_to,
            completion_from=completion_from,
            completion_to=completion_to,
            order_desc=order_desc,
        )
