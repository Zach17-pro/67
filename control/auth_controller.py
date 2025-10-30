from typing import Optional, Dict, Any
from entity.user_repository import UserRepository

class AuthController:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate(self, username: str, password: str, role: str):
        user = self.repo.get_user_by_credentials(username, password, role)
        if not user:
            return None
        return user

    def role_endpoint_for(self, role: str) -> Optional[str]:
        mapping = {
            "Admin": "role_page.Admin",
            "Platform_Manager": "role_page.Platform_Manager",
            "PIN_Support": "role_page.PIN_Support",
            "Csr_Rep": "role_page.Csr_Rep",
        }
        return mapping.get(role)
