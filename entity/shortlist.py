# entity/shortlist.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Shortlist:
  shortlist_id: int
  csr_user_id: int
  request_id: int
  notes: str
  added_at: datetime