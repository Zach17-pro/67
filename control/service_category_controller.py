# app/controllers/platform_manager_controller.py
from typing import List, Dict, Any
from entity.service_category_repository import ServiceCategoryRepository

class ReadServiceCategoryController:
    def __init__(self, repo: ServiceCategoryRepository):
        self.repo = repo
    def read_categories(self) -> List[Dict[str, Any]]:
        return self.repo.list_categories()
    
class CreateServiceCategoryController:
    def __init__(self, repo: ServiceCategoryRepository):
        self.repo = repo
    def create_category(self, name: str) -> int:
        return self.repo.create_category(name)
    
class UpdateServiceCategoryController:
    def __init__(self, repo: ServiceCategoryRepository):
        self.repo = repo
    def update_category(self, category_id: int, name: str) -> None:
        self.repo.update_category(category_id, name)

class DeleteServiceCategoryController:
    def __init__(self, repo: ServiceCategoryRepository):
        self.repo = repo
    def delete_category(self, category_id: int) -> None:
        self.repo.delete_category(category_id)
