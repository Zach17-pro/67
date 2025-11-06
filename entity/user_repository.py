# app/entity/user_repository.py
# User Stories (User Accounts)
#2 As a user admin, I want to create user accounts so that new users can access the system.
#3 As a user admin, I want to view user accounts so that I can retrieve stored information.
#4 As a user admin, I want to update user accounts so that the latest information is stored.
#5 As a user admin, I want to delete user accounts so that unused or invalid accounts are removed.
#6 As a user admin, I want to search for user accounts so that I can quickly locate them.
#
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

    # ---------- Auth ----------
    def get_user_by_credentials(self, username: str, password: str, role: str) -> Optional[UserProfile]:
        """
        Return a UserProfile matching username/password/role, or None.
        Uses a buffered cursor to avoid 'Unread result found'.
        """
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute(
                """
                SELECT user_id, username, full_name, role, email, created_at
                FROM user
                WHERE username = %s AND password = %s AND role = %s
                """,
                (username, password, role),
            )
            row = cur.fetchone()
        finally:
            cur.close()

        if not row:
            return None

        return UserProfile(
            id=row["user_id"],
            username=row["username"],
            full_name=row["full_name"],
            role=row["role"],
            email=row["email"],
            created_at=row["created_at"],
        )

    ###########################
    ###### USER ACCOUNTS ######
    ###########################

    def create_user(self, username: str, password: str, role: str, full_name: str) -> UserProfile:
        cur = self.db.cursor()
        try:
            cur.execute(
                "INSERT INTO user (username, password, role, full_name) VALUES (%s, %s, %s, %s)",
                (username, password, role, full_name),
            )
            self.db.commit()
            new_id = cur.lastrowid
        finally:
            cur.close()

        return UserProfile(id=new_id, username=username, full_name=full_name, role=role)

    def list_users(self) -> List[UserProfile]:
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute("SELECT user_id AS id, username, role FROM user")
            rows = cur.fetchall()
        finally:
            cur.close()

        return [UserProfile(id=row["id"], username=row["username"], role=row["role"]) for row in rows]

    def update_user(self, user_id: int, username: str, role: str, password: Optional[str] = None) -> None:
        cur = self.db.cursor()
        try:
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
        finally:
            cur.close()

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        cur = self.db.cursor()
        try:
            cur.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
            self.db.commit()
        finally:
            cur.close()

        return {"success": True, "deleted_user_id": user_id}

    def search_users(self, keyword: str) -> List[UserProfile]:
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            search_term = f"%{keyword.lower()}%"
            cur.execute(
                """
                SELECT user_id AS id, username, role
                FROM user
                WHERE LOWER(username) LIKE %s
                   OR LOWER(role) LIKE %s
                """,
                (search_term, search_term),
            )
            rows = cur.fetchall()
        finally:
            cur.close()

        return [UserProfile(id=row["id"], username=row["username"], role=row["role"]) for row in rows]

    ###########################
    ###### USER PROFILES ######
    ###########################

    def create_profile(self, username: str, full_name: str, email: str) -> UserProfile:
        cur = self.db.cursor()
<<<<<<< HEAD
        try:
            cur.execute(
                "INSERT INTO user (username, full_name, email) VALUES (%s, %s, %s)",
                (username, full_name, email),
            )
            self.db.commit()
            new_id = cur.lastrowid
        finally:
            cur.close()
=======
        cur.execute(
            "INSERT INTO user (username, full_name, email, password, role) VALUES (%s, %s, %s)",
            (username, full_name, email, 'default123','user'),
        )
        self.db.commit()
        new_id = cur.lastrowid
        cur.close()
>>>>>>> 6de5a2dc97b871fb10c2103c7a3098ab403ef237

        return UserProfile(id=new_id, username=username, full_name=full_name, email=email)

    def list_profiles(self) -> List[UserProfile]:
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            cur.execute("SELECT user_id AS id, username, full_name, email FROM user")
            rows = cur.fetchall()
        finally:
            cur.close()

        profiles = [
            UserProfile(
                id=row["id"],
                username=row["username"],
                full_name=row["full_name"],
                email=row["email"],
            )
            for row in rows
        ]
        return profiles

    def update_profile(self, user_id: int, full_name: str, email: Optional[str]) -> None:
        cur = self.db.cursor()
        try:
            cur.execute(
                "UPDATE user SET full_name = %s, email = %s WHERE user_id = %s",
                (full_name, email, user_id),
            )
            self.db.commit()
        finally:
            cur.close()

    def delete_profile(self, user_id: int) -> Dict[str, Any]:
        cur = self.db.cursor()
        try:
            cur.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
            self.db.commit()
        finally:
            cur.close()

        return {"success": True, "deleted_user_id": user_id}

    def search_profiles(self, keyword: str) -> List[UserProfile]:
        cur = self.db.cursor(dictionary=True, buffered=True)
        try:
            search_term = f"%{keyword.lower()}%"
            cur.execute(
                """
                SELECT user_id AS id, username, full_name, email
                FROM user
                WHERE LOWER(username) LIKE %s
                   OR LOWER(full_name) LIKE %s
                   OR LOWER(email) LIKE %s
                """,
                (search_term, search_term, search_term),
            )
            rows = cur.fetchall()
        finally:
            cur.close()

        return [
            UserProfile(
                id=row["id"],
                username=row["username"],
                full_name=row["full_name"],
                email=row["email"],
            )
            for row in rows
        ]
