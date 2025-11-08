from typing import List, Dict, Optional, Any
from entity.csr_rep_repository import CSRRepRepository

class CSRRepController:
    def __init__(self, repo: CSRRepRepository):
        self.repo = repo

    # 1. List active/open requests
    def list_active_requests(self) -> List[Dict[str, Any]]:
        return self.repo.list_active_requests()

    # 2. Get request details
    def get_request_details(self, request_id: int) -> Optional[Dict[str, Any]]:
        return self.repo.get_request_details(request_id)

    # 3. Shortlist request
    def add_to_shortlist(self, csr_id: int, request_id: int) -> None:
        self.repo.add_to_shortlist(csr_id, request_id)

    # 4. Get shortlist
    def get_shortlist(self, csr_id: int) -> List[Dict[str, Any]]:
        return self.repo.get_shortlist(csr_id)

    # 5. Search shortlist
    def search_shortlist(self, csr_id: int, query: str) -> List[Dict[str, Any]]:
        return self.repo.search_shortlist(csr_id, query)

    # 6. Search past matches
    def search_past_matches(self, service: str = "", start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        return self.repo.search_past_matches(service, start_date, end_date)

    # 7. View past matches
    def get_past_matches(self, service: str = "", start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        return self.repo.get_past_matches(service, start_date, end_date)
