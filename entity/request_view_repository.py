from datetime import datetime
from entity.shortlist import Shortlist
from typing import List, Dict, Optional, Any

class RequestViewRepository:
  
    def __init__(self, db):
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
