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

    def create_user(self, username, password, role):
        """Insert new user into DB."""
        try:
            cursor = self.db.cursor(dictionary=True)
            sql = """
                INSERT INTO user (username, password, role, full_name)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (username, password, role, username))
            self.db.commit()

            user_id = cursor.lastrowid
            cursor.close()

            return {
                "id": user_id,
                "username": username,
                "role": role,
                "full_name": username,
            }
        except Exception as e:
            raise Exception(f"Error creating user: {e}")

    def list_users(self):
        """Retrieve all users."""
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT user_id AS id, username, role, full_name FROM user")
            users = cursor.fetchall()
            cursor.close()
            return users
        except Exception as e:
            raise Exception(f"Error reading users: {e}")
        
    def get_csr(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT user_id AS id, username, role, full_name FROM user WHERE role='Csr_Rep'")
            users = cursor.fetchall()
            cursor.close()
            return users
        except Exception as e:
            raise Exception(f"Error reading users: {e}")
        

    def update_user(self, user_id, username, role, password=None):
        """Update an existing user."""
        try:
            cursor = self.db.cursor()
            if password:
                sql = """
                    UPDATE user SET username = %s, password = %s, role = %s
                    WHERE user_id = %s
                """
                cursor.execute(sql, (username, password, role, user_id))
            else:
                sql = """
                    UPDATE user SET username = %s, role = %s
                    WHERE user_id = %s
                """
                cursor.execute(sql, (username, role, user_id))
            self.db.commit()
            cursor.close()
            return {"success": True, "updated_user_id": user_id}
        except Exception as e:
            raise Exception(f"Error updating user: {e}")

    def delete_user(self, user_id):
        """Delete a user."""
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
            self.db.commit()
            cursor.close()
            return {"success": True, "deleted_user_id": user_id}
        except Exception as e:
            raise Exception(f"Error deleting user: {e}")

    def search_users(self, keyword):
        """Search for users by username or role."""
        try:
            cursor = self.db.cursor(dictionary=True)
            sql = """
                SELECT user_id AS id, username, role, full_name
                FROM user
                WHERE username LIKE %s OR role LIKE %s
            """
            cursor.execute(sql, (f"%{keyword}%", f"%{keyword}%"))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            raise Exception(f"Error searching users: {e}")

    ###########################
    ###### USER PROFILES ######
    ###########################

    def create_profile(self, username, full_name, email, password):
        """Create a new user profile linked to a user account."""
        try:
            cursor = self.db.cursor(dictionary=True)
            sql = """
                INSERT INTO user (username, full_name, email, password)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (username, full_name, email, password))
            self.db.commit()
            profile_id = cursor.lastrowid
            cursor.close()
            return {
                "profile_id": profile_id,
                "username": username,
                "full_name": full_name,
                "email": email,
            }
        except Exception as e:
            raise Exception(f"Error creating profile: {e}")

    def list_profiles(self):
        """Retrieve all user profiles, joined with user accounts."""
        try:
            cursor = self.db.cursor(dictionary=True)
            sql = """
                SELECT user_id AS id, username, role,
                       full_name, email, created_at
                FROM user
            """
            cursor.execute(sql)
            profiles = cursor.fetchall()
            cursor.close()
            return profiles
        except Exception as e:
            raise Exception(f"Error reading profiles: {e}")

    def update_profile(self, profile_id, full_name, email):
        """Update user profile details."""
        try:
            cursor = self.db.cursor()
            sql = """
                UPDATE user
                SET full_name = %s, email = %s
                WHERE user_Id = %s
            """
            cursor.execute(sql, (full_name, email, profile_id))
            self.db.commit()
            cursor.close()
            return {"success": True, "updated_profile_id": profile_id}
        except Exception as e:
            raise Exception(f"Error updating profile: {e}")

    def delete_profile(self, profile_id):
        """Delete a user profile."""
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM user WHERE user_id = %s", (profile_id,))
            self.db.commit()
            cursor.close()
            return {"success": True, "deleted_profile_id": profile_id}
        except Exception as e:
            raise Exception(f"Error deleting profile: {e}")
        
    def search_profiles(self, keyword):
        """Search for profiles by username, full name, or email."""
        try:
            cursor = self.db.cursor(dictionary=True)
            sql = """
                SELECT p.user_id AS id, u.username, u.role,
                       p.full_name, p.email
                FROM user p
                WHERE p.username LIKE %s
                   OR p.full_name LIKE %s
                   OR p.email LIKE %s
                   OR p.role LIKE %s
            """
            like = f"%{keyword}%"
            cursor.execute(sql, (like, like, like, like))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            raise Exception(f"Error searching profiles: {e}")