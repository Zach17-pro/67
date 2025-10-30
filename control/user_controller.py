from typing import List, Dict, Any, Optional
from entity.user_repository import UserRepository

class UserController:
    def __init__(self, repo: UserRepository):
        self.repo = repo