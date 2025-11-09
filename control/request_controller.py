# app/controllers/pin_request_controller.py
from __future__ import annotations

from typing import List, Optional, Dict, Any
from datetime import datetime
from entity.pin_request import Request
from entity.pin_request_repository import RequestRepository
from entity.match_repository import MatchRepository
from utility.request_validation import RequestValidation

ALLOWED_STATUSES = {"Open", "In Progress", "Completed", "Cancelled"} 

class SearchPinRequestController:
    def __init__(self, pin_req_repo: RequestRepository):
        self.pin_req_repo = pin_req_repo
    # 1. List active/open requests
    def list_active_requests(self, search) -> List[Dict[str, Any]]:
        return self.pin_req_repo.search_requests_by_status(status = ('Open', 'In Progress'), query=search)

class ReadRequestController:
    def __init__(self, request_repo):
        self.request_repo = request_repo

    def read_request(self, *, request_id: int):
        RequestValidation._require_positive_id(request_id, "pin_user_id")
        self.request_repo.get_increment_request_view(request_id)
        return self.request_repo.get_request_by_id(request_id)

class CreatePinRequestController:
    def __init__(self, request_repo, match_repo: Optional[object] = None):
        self.request_repo = request_repo
        self.match_repo = match_repo  

    # -------- #23: Create a request --------
    def create_request(
        self,
        *,
        pin_user_id: int,
        title: str,
        description: str,
        location: str,
        category_id: Optional[int] = None,
    ):
        RequestValidation._require_positive_id(pin_user_id, "pin_user_id")
        RequestValidation._require_text(title, "title")
        RequestValidation._require_text(description, "description")
        RequestValidation._require_text(location, "location")
        if category_id is not None:
            RequestValidation._require_positive_id(category_id, "category_id")  # [web:33][web:46]

        return self.request_repo.create_request(
            pin_user_id=pin_user_id,
            title=title.strip(),
            description=description.strip(),
            category_id=category_id,
            location=location.strip(),
        )  # [web:44][web:50]

    # -------- #24: View my requests --------
class ListMyPinRequestsController:
    def __init__(self, request_repo, match_repo: Optional[object] = None):
        self.request_repo = request_repo
        self.match_repo = match_repo  # unused here but kept for parity  # [web:44][web:50]

    # -------- #24: View my requests --------
    def list_my_requests(
        self, *, pin_user_id: int, status: Optional[str] = None, order_desc: bool = True
    ):
        RequestValidation._require_positive_id(pin_user_id, "pin_user_id")
        if status is not None:
            RequestValidation._require_status(status)
        return self.request_repo.list_requests_by_pin(
            pin_user_id=pin_user_id, status=status, order_desc=order_desc
        )  # [web:44][web:50]

    # -------- #25: Update my request --------
class UpdatePinRequestController:
    def __init__(self, request_repo, match_repo: Optional[object] = None):
        self.request_repo = request_repo
        self.match_repo = match_repo  # used here for ensure_completed_match  # [web:44][web:58]

    # -------- #25: Update my request --------
    def update_request(
        self,
        *,
        pin_user_id: int,
        request_id: int,
        csr_user_id: Optional[str],
        title: Optional[str] = None,
        description: Optional[str] = None,
        category_id: Optional[int] = None,
        location: Optional[str] = None,
        status: Optional[str] = None,
    ):
        RequestValidation._require_positive_id(pin_user_id, "pin_user_id")
        RequestValidation._require_positive_id(request_id, "request_id")
        if title is not None:
            RequestValidation._require_text(title, "title")
        if description is not None:
            RequestValidation._require_text(description, "description")
        if location is not None:
            RequestValidation._require_text(location, "location")
        if category_id is not None:
            RequestValidation._require_positive_id(category_id, "category_id")
        if status is not None:
            RequestValidation._require_status(status)  # [web:33][web:46]

        updated = self.request_repo.update_request(
            request_id=request_id,
            pin_user_id=pin_user_id,
            title=title.strip() if isinstance(title, str) else title,
            description=description.strip() if isinstance(description, str) else description,
            category_id=category_id,
            location=location.strip() if isinstance(location, str) else location,
            status=status,
        )  # [web:44][web:50]
    
        # If the request was (or is now) Completed, ensure a Completed match row exists.
        # NOTE: We use pin_user_id as a placeholder csr_user_id if none is known.
        #       Replace with the actual CSR id when you have it in your flow.
        if updated and status == "Completed" and self.match_repo is not None:
            try:
                self.match_repo.ensure_completed_match(
                    request_id=request_id,
                    pin_user_id=pin_user_id,
                    csr_user_id=csr_user_id,  # TODO: provide real CSR user id when available
                )
            except Exception:
                # Don't block the request update if match creation fails; surface via logs if desired.
                pass  # [web:44][web:58]

        return updated


    # -------- #26: Delete my request --------
class DeleteMyPinRequestController:
    def __init__(self, request_repo, match_repo: Optional[object] = None):
        self.request_repo = request_repo
        self.match_repo = match_repo  # unused here but kept for parity  # [web:44][web:50]

    # -------- #26: Delete my request --------
    def delete_request(self, *, pin_user_id: int, request_id: int) -> bool:
        RequestValidation._require_positive_id(pin_user_id, "pin_user_id")
        RequestValidation._require_positive_id(request_id, "request_id")
        deleted = self.request_repo.delete_request(request_id=request_id, pin_user_id=pin_user_id)
        return deleted is not None  # [web:44][web:50]

    # -------- #27: Search my requests --------
class SearchMyPinRequestsController:
    def __init__(self, request_repo, match_repo: Optional[object] = None):
        self.request_repo = request_repo
        self.match_repo = match_repo  # unused here but kept for parity  # [web:44][web:50]

    # -------- #27: Search my requests --------
    def search_my_requests(
        self,
        *,
        pin_user_id: int,
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        category_id: Optional[int] = None,
        date_from: Optional[datetime | str] = None,
        date_to: Optional[datetime | str] = None,
        order_desc: bool = True,
    ):
        RequestValidation._require_positive_id(pin_user_id, "pin_user_id")
        if status is not None:
            RequestValidation._require_status(status)
        if category_id is not None:
            RequestValidation._require_positive_id(category_id, "category_id")  # [web:33][web:46]

        dt_from = RequestValidation._parse_dt(date_from) if date_from else None
        dt_to = RequestValidation._parse_dt(date_to) if date_to else None
        RequestValidation._require_dt_order(dt_from, dt_to)  # [web:51][web:48]

        return self.request_repo.search_user_requests(
            pin_user_id=pin_user_id,
            keyword=(keyword.strip() if isinstance(keyword, str) and keyword.strip() else None),
            status=status,
            category_id=category_id,
            date_from=dt_from,
            date_to=dt_to,
            order_desc=order_desc,
        ) 
    
    