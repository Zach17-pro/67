from dataclasses import dataclass
from datetime import datetime

# User Account
@dataclass
class UserAccount:
  username: str
  password: str

# User Profile
@dataclass
class UserProfile:
  id: int
  username: str
  full_name: str
  role: str
  email: str
  created_at: datetime