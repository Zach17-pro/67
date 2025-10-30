# app/controllers/platform_manager_controller.py
from typing import List, Dict, Any
from entity.service_category_repository import ServiceCategoryRepository

class ServiceCategoryController:
    def __init__(self, repo: ServiceCategoryRepository):
        self.repo = repo

    def read_categories(self) -> List[Dict[str, Any]]:
        return self.repo.list_categories()

    def create_category(self, name: str) -> int:
        return self.repo.create_category(name)

    def update_category(self, category_id: int, name: str) -> None:
        self.repo.update_category(category_id, name)

    def delete_category(self, category_id: int) -> None:
        self.repo.delete_category(category_id)
