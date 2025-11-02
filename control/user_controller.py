# app/control/user_controller.py
# User Stories (User Accounts)
#2 As a user admin, I want to create user accounts so that new users can access the system.
#3 As a user admin, I want to view user accounts so that I can retrieve stored information.
#4 As a user admin, I want to update user accounts so that the latest information is stored.
#5 As a user admin, I want to delete user accounts so that unused or invalid accounts are removed.
#6 As a user admin, I want to search for user accounts so that I can quickly locate them.

# User Stories (User Profiles)
#7 As a user admin, I want to create user profiles so that users’ details are recorded.
#8 As a user admin, I want to view user profiles so that I can check stored information.
#9 As a user admin, I want to update user profiles so that details remain current.
#10 As a user admin, I want to delete user profiles so that invalid records are removed.
#11 As a user admin, I want to search user profiles so that I can retrieve specific information quickly.

from typing import List, Dict, Any
from entity.user_repository import UserRepository

class UserController:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    ###########################
    ###### USER ACCOUNTS ######
    ###########################

    #2 As a user admin, I want to create user accounts so that new users can access the system.
    def create_user(self, username: str, password: str, role: str, full_name: str):
        return self.repo.create_user(username, password, role, full_name)

    #3 As a user admin, I want to view user accounts so that I can retrieve stored information.
    def list_users(self):
        return self.repo.list_users()

    #4 As a user admin, I want to update user accounts so that the latest information is stored.
    def update_user(self, user_id: int, username: str, role: str, password: str = None):
        return self.repo.update_user(user_id, username, role, password)

    #5 As a user admin, I want to delete user accounts so that unused or invalid accounts are removed.
    def delete_user(self, user_id: int):
        return self.repo.delete_user(user_id)

    #6 As a user admin, I want to search for user accounts so that I can quickly locate them.
    def search_users(self, keyword: str):
        # simple search: match username or role (can be improved)
        all_users = self.repo.list_users()
        return [
            u for u in all_users
            if keyword.lower() in u.username.lower() or keyword.lower() in u.role.lower()
        ]
        
    ###########################
    ###### USER PROFILES ######
    ###########################
    
    #7 As a user admin, I want to create user profiles so that users’ details are recorded.
    def create_profile(self, username: str, full_name: str, email: str):
        return self.repo.create_user(username=username, password="default123", role="user", full_name=full_name)
    
    #8 As a user admin, I want to view user profiles so that I can check stored information.
    def list_profiles(self):
        return self.repo.list_profiles()

    #9 As a user admin, I want to update user profiles so that details remain current.
    def update_profile(self, user_id: int, full_name: str, email: str):
        return self.repo.update_profile(user_id, full_name, email)

    #10 As a user admin, I want to delete user profiles so that invalid records are removed.
    def delete_profile(self, user_id: int):
        return self.repo.delete_user(user_id)

    #11 As a user admin, I want to search user profiles so that I can retrieve specific information quickly.
    def search_profiles(self, keyword: str):
        return self.repo.search_profiles(keyword)