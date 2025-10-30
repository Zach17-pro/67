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
        return UserProfile(id=row["user_id"], username=row['username']
                           , full_name=row['full_name'], role=row['role']
                           , email=row['email'], created_at=row['created_at'])

    def list_users(self):
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT user_id AS id, username, role FROM user")
        rows = cur.fetchall()
        cur.close()
        return [UserProfile(id=row["id"], username=row['username'], role=row['role']) for row in rows]

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

    def delete_user(self, user_id: int):
        cur = self.db.cursor()
        cur.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
        self.db.commit()
        cur.close()

    def list_profiles(self):
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT user_id AS id, username, full_name, email FROM user")
        rows = cur.fetchall()
        cur.close()
        categories = [UserProfile(id=row["id"], username=row["username"], full_name=row["full_name"], email=row["email"]) for row in rows]
        return categories

    def update_profile(self, user_id: int, full_name: str, email: Optional[str]):
        cur = self.db.cursor()
        cur.execute(
            "UPDATE user SET full_name = %s, email = %s WHERE user_id = %s",
            (full_name, email, user_id),
        )
        self.db.commit()
        cur.close()
