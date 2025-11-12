from dataclasses import dataclass
from datetime import datetime

# User Account
@dataclass
class UserAccount:
  id: int
  username: str
  role: str
  password: str

# User Profile
@dataclass
class UserProfile:
  id: int
  username: str
  full_name: str
  email: str
  role: str
  created_at: datetime