from datetime import datetime

from flask import current_app
from entity.shortlist import Shortlist
from typing import List, Dict, Optional, Any

class RequestViewRepository:
  
    def __init__(self):
        db = current_app.config["DB"]
        self.db = db


    def save_view(self, request_id: int, timestamp: datetime) -> None:
            cur = self.db.cursor()
            try:
                cur.execute(
                    "INSERT INTO request_view (request_id, viewed_at) VALUES (%s, %s)",
                    (request_id, timestamp)
                )
                self.db.commit()
            finally:
                cur.close()

    def count_views(self, frm: datetime, to: datetime) -> int:
        sql = "SELECT COUNT(*) FROM request_view WHERE viewed_at >= %s AND viewed_at < %s"
        with self.db.cursor() as cur:
            cur.execute(sql, (frm, to))
            return int(cur.fetchone()[0])