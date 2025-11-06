# app/entity/service_category_repository.py
from typing import List, Dict, Any, Optional, Tuple
from mysql.connector import errorcode, errors


class ServiceCategoryRepository:
    def __init__(self, db):
        self.db = db

    # ---------- Read ----------
    def list_categories(self) -> List[Dict[str, Any]]:
        """
        Return simple JSON-ready dicts: [{id, name}, ...]
        """
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute(
                "SELECT category_id AS id, category_name AS name FROM service_category"
            )
            rows = cur.fetchall()
            return rows  # already dicts with {id, name}
        finally:
            cur.close()

    # ---------- Create ----------
    def create_category(self, name: str) -> int:
        """
        Create a category and return its new integer id.
        """
        cur = self.db.cursor()
        try:
            cur.execute(
                "INSERT INTO service_category (category_name) VALUES (%s)", (name,)
            )
            self.db.commit()
            return cur.lastrowid
        finally:
            cur.close()

    # ---------- Update ----------
    def update_category(self, category_id: int, name: str) -> None:
        cur = self.db.cursor()
        try:
            cur.execute(
                "UPDATE service_category SET category_name = %s WHERE category_id = %s",
                (name, category_id),
            )
            self.db.commit()
        finally:
            cur.close()

    # ---------- Delete ----------
    def delete_category(self, category_id: int) -> None:
        """
        Try to delete a category. If it is referenced by requests/matches,
        raise a friendly ValueError with counts.
        """
        req_count, match_count = self._count_refs(category_id)
        if req_count or match_count:
            # Friendly app-level error before hitting FK constraint
            raise ValueError(
                f"Cannot delete: category {category_id} is used by "
                f"{req_count} request(s) and {match_count} match(es)."
            )

        cur = self.db.cursor()
        try:
            cur.execute("DELETE FROM service_category WHERE category_id = %s", (category_id,))
            self.db.commit()
        except errors.IntegrityError as e:
            # Fallback in case of race conditions or other FK paths
            if getattr(e, "errno", None) == errorcode.ER_ROW_IS_REFERENCED_2:  # 1451
                raise ValueError(
                    "Cannot delete category: it is still referenced by existing records."
                ) from e
            raise
        finally:
            cur.close()

    # ---------- Internals ----------
    def _count_refs(self, category_id: int) -> Tuple[int, int]:
        """
        Return (requests_using_category, matches_using_category).
        matches are counted via request -> match join.
        """
        cur = self.db.cursor(buffered=True)
        try:
            # Requests that point to this category
            cur.execute("SELECT COUNT(*) FROM request WHERE category_id = %s", (category_id,))
            req_count = cur.fetchone()[0]

            # Matches that involve requests with this category
            cur.execute(
                """
                SELECT COUNT(*)
                FROM `match` m
                JOIN request r ON r.request_id = m.request_id
                WHERE r.category_id = %s
                """,
                (category_id,),
            )
            match_count = cur.fetchone()[0]
            return req_count, match_count
        finally:
            cur.close()
