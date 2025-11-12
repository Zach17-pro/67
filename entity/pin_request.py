# entity/request.py
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime
from entity.service_category import ServiceCategory

@dataclass
class Request:
    request_id: int
    pin_user_id: int
    title: str
    description: str
    status: str  # 'Open' | 'In Progress' | 'Completed' | 'Cancelled'
    created_at: datetime
    updated_at: datetime
    view_count: int
    shortlist_count: int
    location: str
    category: Optional[ServiceCategory] = None
    category_id: Optional[int] = None

    def set_service_category(self, category: Optional[ServiceCategory]) -> None:
        self.category = category

    @staticmethod
    def _row_to_request(row: Dict[str, Any]) -> "Request":
        req = Request(
            request_id=row["request_id"],
            pin_user_id=row["pin_user_id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            view_count=row["view_count"],
            category_id=row["category_id"],
            shortlist_count=row["shortlist_count"],
            location=row["location"]
        )
        return req

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Request":
        category = None
        category_id = data.get("category_id")

        if "category" in data:
            cat = data["category"]
            if isinstance(cat, ServiceCategory):
                category = cat
                category_id = cat.category_id
            elif isinstance(cat, dict):
                category = ServiceCategory(
                    category_id=cat.get("category_id"),
                    name=cat.get("name"),
                )
                category_id = category.category_id

        return cls(
            request_id=data["request_id"],
            pin_user_id=data["pin_user_id"],
            title=data["title"],
            description=data["description"],
            status=data["status"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            view_count=data["view_count"],
            shortlist_count=data["shortlist_count"],
            location=data["location"],
            category=category,
            category_id=category_id,
        )
    