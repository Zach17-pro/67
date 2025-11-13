#14
# As a CSR Rep, I want to search for PIN requests so that I can find opportunities to support.
#15
# As a CSR Rep, I want to view details of a PIN request so that I can evaluate suitability.
#23
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

#32
# As a PIN, I want to view the number of times my request has been viewed so that I can gauge interest

from typing import List, Optional, Any, Dict
from datetime import datetime

from flask import current_app
from entity.pin_request import Request
from entity.match_repository import MatchRepository


class RequestRepository:
    """
    Entity-focused repository for PIN request flows.
    Covers user stories:
      #23 create, #24 view mine, #25 update, #26 delete,
      #27 search mine, #28 search past matches, #29 view past matches
    """
    def __init__(self):
        db = current_app.config["DB"]
        self.db = db

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
        cur = self.db.cursor(dictionary=True)
        if pin_user_id is None:
            cur.execute(
                """
                SELECT
                r.*,
                COALESCE(sl.cnt, 0) AS shortlist_count,
                COALESCE(rv.cnt, 0) AS view_count
                FROM request r
                LEFT JOIN (
                SELECT request_id, COUNT(*) AS cnt
                FROM shortlist
                GROUP BY request_id
                ) sl ON sl.request_id = r.request_id
                LEFT JOIN (
                SELECT request_id, COUNT(*) AS cnt
                FROM request_view
                GROUP BY request_id
                ) rv ON rv.request_id = r.request_id
                WHERE r.request_id = %s;
                """,
                (request_id,),
            )
        else:
            cur.execute(
                """
                SELECT
                r.*,
                COALESCE(sl.cnt, 0) AS shortlist_count,
                COALESCE(rv.cnt, 0) AS view_count
                FROM request r
                LEFT JOIN (
                SELECT request_id, COUNT(*) AS cnt
                FROM shortlist
                GROUP BY request_id
                ) sl ON sl.request_id = r.request_id
                LEFT JOIN (
                SELECT request_id, COUNT(*) AS cnt
                FROM request_view
                GROUP BY request_id
                ) rv ON rv.request_id = r.request_id
                WHERE r.request_id = %s AND r.pin_user_id = %s;
                """
                ,
                (request_id, pin_user_id),
            )
        row = cur.fetchone()
        cur.close()
        return (row) if row else None

    # ---------- #24: View my requests ----------
    def list_requests_by_pin(
        self,
        pin_user_id: int,
        status: Optional[str] = None,
        order_desc: bool = True,
    ) -> List[Request]:
        try:
            """
            Returns all requests for a PIN (optionally filtered by status).
            """
            params: List[Any] = [pin_user_id]
            sql = """
            SELECT
            r.*,
            COALESCE(sl.cnt, 0) AS shortlist_count,
            COALESCE(rv.cnt, 0) AS view_count
            FROM request r
            LEFT JOIN (
            SELECT request_id, COUNT(*) AS cnt
            FROM shortlist
            GROUP BY request_id
            ) sl ON sl.request_id = r.request_id
            LEFT JOIN (
            SELECT request_id, COUNT(*) AS cnt
            FROM request_view
            GROUP BY request_id
            ) rv ON rv.request_id = r.request_id
            WHERE r.pin_user_id = %s
            """
            params = [pin_user_id]
            if status:
                sql += " AND r.status = %s"
                params.append(status)
            sql += " ORDER BY r.created_at " + ("DESC" if order_desc else "ASC")            
            cur = self.db.cursor(dictionary=True)
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            cur.close()
            return [(r) for r in rows]
        except Exception as e:
            print(str(e))

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
        Deletes a request owned by the PIN *only if* there are no dependent matches.
        Returns a minimal Request with request_id if deleted, else None.
        Raises ValueError when blocked by dependencies.
        """
        # local import to avoid changing module imports
        from mysql.connector import errors as db_errors

        # Verify ownership / existence first
        existing = self.get_request_by_id(request_id, pin_user_id)
        if not existing:
            return None

        cur = self.db.cursor()
        try:
            # Guard: refuse delete if there are matches referencing this request
            cur.execute("SELECT COUNT(*) FROM `match` WHERE request_id = %s", (request_id,))
            cnt_row = cur.fetchone()
            # plain cursor returns a tuple like (count,)
            dep_count = (cnt_row[0] if cnt_row else 0)
            if dep_count and dep_count > 0:
                cur.execute("DELETE FROM `match` WHERE request_id = %s",
                (request_id, ),
            )

            # Proceed with deletion
            cur.execute(
                "DELETE FROM request WHERE request_id = %s AND pin_user_id = %s",
                (request_id, pin_user_id),
            )
            self.db.commit()

            if cur.rowcount == 0:
                # nothing deleted (race condition or ownership mismatch)
                return None

            # Return a copy of the deleted item's key fields (your existing pattern)
            return True
        except Exception as e:
            # any other FK blocks
            print("Error:",str(e))
            self.db.rollback()
            raise ValueError("Request cannot be deleted because it is referenced by other records.") from e
        finally:
            cur.close()

    # ---------- #27: Search my requests ----------
    def search_user_requests(
        self,
        pin_user_id: Optional[int],
        *,
        keyword: Optional[str] = None,       # matches title/description
        status = None,
        category_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        order_desc: bool = True,
    ) -> List[Request]:
        """
        Search a PIN's requests using common filters.
        """
        sql = """
            SELECT *
            FROM request
            WHERE pin_user_id = %s
        """
        
        params: List[Any] = [pin_user_id]
    
        if keyword:
            sql += " AND (title LIKE %s OR description LIKE %s)"
            like = f"%{keyword}%"
            params.extend([like, like])

        if status:
            if isinstance(status, (list, tuple)):
                placeholders = ", ".join(["%s"] * len(status))
                sql += f" AND status IN ({placeholders})"
                params.extend(list(status))
            else:
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
        return [(r) for r in rows]
    
    def search_requests_by_status(
        self,
        *,
        status = None,
        query = "",
        order_desc: bool = True,
    ) -> List[Request]:
        """
        Search a PIN's requests using common filters.
        """
        sql = f"""
            SELECT r.request_id, r.pin_user_id, r.title, r.description, r.status,
                   r.created_at, r.updated_at, r.shortlist_count,
                   r.category_id, r.location, COALESCE(COUNT(rv.view_id), 0) AS view_count
            FROM request r
            LEFT JOIN request_view AS rv ON rv.request_id = r.request_id
            Where
        """

        params = []

        # Support single status (string) or multiple (list/tuple)
        if status:
            if isinstance(status, (list, tuple)):
                placeholders = ", ".join(["%s"] * len(status))
                sql += f" status IN ({placeholders})"
                params.extend(list(status))
            else:
                sql += " status = %s"
                params.append(status)
                
        print(query)
        sql += " AND (r.title LIKE %s OR r.description LIKE %s)"
        params.append(f"%{query}%")
        params.append(f"%{query}%")

        sql += " GROUP BY r.request_id ORDER BY created_at " + ("DESC" if order_desc else "ASC")
        

        cur = self.db.cursor(dictionary=True)
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        cur.close()
        return [(r) for r in rows]


    def count_created(self, frm: datetime, to: datetime) -> int:
        sql = "SELECT COUNT(*) FROM request WHERE created_at >= %s AND created_at < %s"
        with self.db.cursor() as cur:
            cur.execute(sql, (frm, to))
            return int(cur.fetchone()[0])

    def status_snapshot(self, frm: datetime, to: datetime) -> List[Dict]:
        sql = "SELECT status, COUNT(*) AS count FROM request WHERE created_at >= %s AND created_at < %s GROUP BY status"
        with self.db.cursor(dictionary=True) as cur:
            cur.execute(sql, (frm, to))
            return list(cur.fetchall())
    
    def count_by_category(self, frm: datetime, to: datetime, include_zero: bool = True) -> List[Dict]:
        if include_zero:
            sql = """
                SELECT sc.category_id,
                       sc.category_name,
                       COUNT(r.request_id) AS count
                FROM service_category sc
                LEFT JOIN request r
                  ON r.category_id = sc.category_id
                 AND r.created_at >= %s AND r.created_at < %s
                GROUP BY sc.category_id, sc.category_name
                ORDER BY count DESC, sc.category_name
            """
            params = (frm, to)
        else:
            sql = """
                SELECT r.category_id,
                       sc.category_name,
                       COUNT(*) AS count
                FROM request r
                JOIN service_category sc ON sc.category_id = r.category_id
                WHERE r.created_at >= %s AND r.created_at < %s
                GROUP BY r.category_id, sc.category_name
                ORDER BY count DESC, sc.category_name
            """
            params = (frm, to)

        with self.db.cursor(dictionary=True) as cur:
            cur.execute(sql, params)
            return list(cur.fetchall())

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
