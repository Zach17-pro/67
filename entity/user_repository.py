# app/entity/user_repository.py
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

from typing import List, Optional, Dict, Any
from entity.user import UserProfile, UserAccount

class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user_by_credentials(self, username: str, password: str, role: str):
        cur = self.db.cursor(dictionary=True)
        cur.execute(
            "SELECT user_id, username, full_name, role, email, created_at FROM user WHERE username = %s AND password = %s AND role = %s",
            (username, password, role),
        )
        row = cur.fetchone()
        cur.close()
        if not(row):
            return None
        user = UserProfile(id=row["user_id"], username=row['username']
                           , full_name=row['full_name'], role=row['role']
                           , email=row['email'], created_at=row['created_at'])
        return user

    ###########################
    ###### USER ACCOUNTS ######
    ###########################

    #2 As a user admin, I want to create user accounts so that new users can access the system.
    def create_user(self, username: str, password: str, role: str, full_name: str):
        cur = self.db.cursor()
        cur.execute(
            "INSERT INTO user (username, password, role, full_name) VALUES (%s, %s, %s, %s)",
            (username, password, role, full_name),
        )
        self.db.commit()
        new_id = cur.lastrowid
        cur.close()
        return UserProfile(id=new_id, username=username
                           , full_name=full_name, role=role)
    
    #3 As a user admin, I want to view user accounts so that I can retrieve stored information.
    def list_users(self):
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT user_id AS id, username, role FROM user")
        rows = cur.fetchall()
        cur.close()
        return [UserProfile(id=row["id"], username=row['username'], role=row['role']) for row in rows]

    #4 As a user admin, I want to update user accounts so that the latest information is stored.
    def update_user(self, user_id: int, username: str, role: str, password: Optional[str] = None):
        cur = self.db.cursor()
        if password:
            cur.execute(
                "UPDATE user SET username = %s, password = %s, role = %s WHERE user_id = %s",
                (username, password, role, user_id),
            )
        else:
            cur.execute(
                "UPDATE user SET username = %s, role = %s WHERE user_id = %s",
                (username, role, user_id),
            )
        self.db.commit()
        cur.close()

    #5 As a user admin, I want to delete user accounts so that unused or invalid accounts are removed.
    def delete_user(self, user_id: int):
        cur = self.db.cursor()
        cur.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
        self.db.commit()
        cur.close()

    #6 As a user admin, I want to search for user accounts so that I can quickly locate them.
    def search_users(self, keyword: str):
        cur = self.db.cursor(dictionary=True)
        search_term = f"%{keyword}%"
        cur.execute(
            "SELECT user_id AS id, username, role FROM user WHERE username LIKE %s OR role LIKE %s",
            (search_term, search_term),
        )
        
        rows = cur.fetchall()
        cur.close()
        return [UserProfile(id=row["id"], username=row['username'], role=row['role']) for row in rows]


    ###########################
    ###### USER PROFILES ######
    ###########################

    #7 As a user admin, I want to create user profiles so that users’ details are recorded.
    def create_profile(self, username: str, full_name: str, email: str):
        cur = self.db.cursor()
        cur.execute(
            "INSERT INTO user (username, full_name, email, role, password) VALUES (%s, %s, %s, %s, %s)",
            (username, full_name, email, "user", "default123"),  # default role and password
        )
        self.db.commit()
        new_id = cur.lastrowid
        cur.close()

        # Return a new UserProfile object
        return UserProfile(id=new_id, username=username, full_name=full_name, email=email)

    #8 As a user admin, I want to view user profiles so that I can check stored information.
    def list_profiles(self):
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT user_id AS id, username, full_name, email FROM user")
        rows = cur.fetchall()
        cur.close()
        categories = [UserProfile(id=row["id"], username=row["username"], full_name=row["full_name"], email=row["email"]) for row in rows]
        return categories

    #9 As a user admin, I want to update user profiles so that details remain current.
    def update_profile(self, user_id: int, full_name: str, email: Optional[str]):
        cur = self.db.cursor()
        cur.execute(
            "UPDATE user SET full_name = %s, email = %s WHERE user_id = %s",
            (full_name, email, user_id),
        )
        self.db.commit()
        cur.close()
    
    #11 As a user admin, I want to search user profiles so that I can retrieve specific information quickly.
    def search_profiles(self, keyword: str):
        cur = self.db.cursor(dictionary=True)
        search_term = f"%{keyword}%"
        cur.execute(
            "SELECT user_id AS id, username, full_name, email FROM user WHERE username LIKE %s OR full_name LIKE %s OR email LIKE %s",
            (search_term, search_term, search_term),
        )
        rows = cur.fetchall()
        cur.close()
        return [UserProfile(id=row["id"], username=row["username"], full_name=row["full_name"], email=row["email"]) for row in rows]