from datetime import datetime
from typing import Optional, List, Dict, Any
from entity.shortlist_repository import ShortlistRepository

class SaveShortlistController:
    def __init__(self, shortlist_repo: ShortlistRepository):
        self.shortlist_repo = shortlist_repo
    # 1. Shortlist request
    def toggle_shortlist(self, csr_id: int, request_id: int, notes: Optional[str]) -> None:
        if (self.shortlist_repo.get_shortlist_by_userid_and_requestid(csr_id, request_id)):
            self.shortlist_repo.delete_shortlist_by_userid_and_requestid(csr_id, request_id)
            print("Delete")
            return
        added_at = datetime.now()
        self.shortlist_repo.save_shortlist(csr_id, request_id, notes, added_at)
        print("Save")

class ViewShortlistController:
    def __init__(self, shortlist_repo: ShortlistRepository):
        self.shortlist_repo = shortlist_repo
    # 2. Get shortlist
    def get_shortlist(self, csr_id: int, search: str) -> List[Dict[str, Any]]:
        return self.shortlist_repo.view_shortlist(csr_id=csr_id, query = search)

class SearchShortlistController:
    def __init__(self, shortlist_repo: ShortlistRepository):
        self.shortlist_repo = shortlist_repo
    # 3. Search shortlist
    def search_shortlist(self, csr_id: int, query: str) -> List[Dict[str, Any]]:
        return self.shortlist_repo.search_shortlist(csr_id, query)

    