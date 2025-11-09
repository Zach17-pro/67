# WARNING: RUNNING THIS FILE CLEARS DATABASE

import mysql.connector
import random 
from faker import Faker

#Config
tables_to_truncate = ['user']

fake = Faker()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="SixSeven"
)

cur = db.cursor()
cur.execute("SET FOREIGN_KEY_CHECKS = 0") 

for t in tables_to_truncate:
    cur.execute(f"TRUNCATE TABLE `{t}`") 

cur.execute("SET FOREIGN_KEY_CHECKS = 1") 
db.commit()
cur.close()

# POPULATE: USER DATA
def create_user(password, email, username, role, created_at, fullname=None):
        """Insert new user into DB."""
        try:
            if fullname:
                fullname = username
            cursor = db.cursor()
            sql = """
                INSERT INTO user (password, email, username, role, full_name, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (password, email, username, role, fullname, created_at))
            db.commit()

            user_id = cursor.lastrowid
            cursor.close()

            return {
                "id": user_id,
                "username": username,
                "role": role,
                "full_name": fullname,
            }
        except Exception as e:
            raise Exception(f"Error creating user: {e}")
        
users_to_create = [('1','admin@email.c','SystemAdmin','Admin','2025-10-20 04:04:41'),
                   ('11','csr@email.com','CSR','Platform_Manager','2025-10-20 04:04:41'),
                   ('pin123','pin@email.com','pin01','PIN_Support','2025-10-20 04:04:41'),
                   ('2','mgr@email.com','mgr','Platform_Manager','2025-10-20 04:04:41'),
                   ('1', None, 'ganbf','Admin','2025-10-20 11:26:35')]

roles = ['Admin','Csr_Rep','PIN_Support','Platform_Manager']
for i in range(100):
    username = fake.unique.user_name()[:50]
    email = fake.unique.ascii_email()[:100]  
    # password = fake.password(length=12)[:255] 
    password = 'password' 
    role = random.choice(roles)  
    full_name = fake.name()[:100]
    created_at = fake.date_time_this_year()
    users_to_create.append((password, email, username, role, created_at, full_name))

for user in users_to_create:
    print("Created user:", create_user(*user))







db.close()