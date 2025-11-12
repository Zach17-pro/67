# WARNING: RUNNING THIS FILE CLEARS DATABASE

from typing import Optional
import mysql.connector
import random 
from faker import Faker
from datetime import datetime, timedelta
import sys
#Config
tables_to_truncate = ['user', 'service_category', 'request', 'shortlist', "request_view", "match"]
data_count = dict.fromkeys(tables_to_truncate, 0)
number_of_request_to_generate = 200

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

def random_datetime_this_year(furthest_day = 30):
    now = datetime.now()
    start = now - timedelta(days=furthest_day)
    created = fake.date_time_between(start_date=start, end_date=now)
    # updated_at strictly after created_at by 1 minute to 60 days
    delta = timedelta(
        minutes=random.randint(1, 60),
    ) + timedelta(days=random.randint(0, 60))
    updated = min(created + delta, now)
    if updated <= created:
        updated = created + timedelta(minutes=1)
    return created, updated

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
                   ('11','csr@email.com','CSR','Csr_Rep','2025-10-20 04:04:41'),
                   ('pin123','pin@email.com','pin01','PIN_Support','2025-10-20 04:04:41'),
                   ('2','mgr@email.com','mgr','Platform_Manager','2025-10-20 04:04:41'),
                   ('1', None, 'ganbf','Admin','2025-10-20 11:26:35')]

roles = ['Csr_Rep','PIN_Support']
for i in range(100):
    username = fake.unique.user_name()[:50]
    email = fake.unique.ascii_email()[:100]  
    # password = fake.password(length=12)[:255] 
    password = 'password' 
    role = random.choice(roles)  
    full_name = fake.name()[:100]
    created_at, updated_at = random_datetime_this_year(40)
    users_to_create.append((password, email, username, role, created_at, full_name))

user_by_role = {
     'Admin': [], 'Csr_Rep': [], 'PIN_Support': [], 'Platform_Manager': []
}

for user in users_to_create:
    data = create_user(*user)
    print("Created user:", data)
    user_by_role[data['role']].append(data)

# POPULATE: CATEGORY DATA
def create_category(id, name):
        try:
            cursor = db.cursor()
            sql = """
                INSERT INTO service_category (category_id, category_name)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (id, name))
            db.commit()

            id = cursor.lastrowid
            cursor.close()

            return {
                "id": id,
                "category_name": name,
            }
        except Exception as e:
            raise Exception(f"Error creating user: {e}")

# AVOID CHANGING THANKS :)
category = ['Climate Action and Energy', 'Education and Scholarships'
                      , 'Shelter', 'Senior Support', 'Disability Support'
                      , 'Digital Inclusion', 'Emergency Support'
                      , 'Hunger Relief', 'Fundraising', 'Arts and Culture']

for index in range(len(category)):
    print("Created category:", create_category(index+1, category[index]))

# POPULATE: REQUEST DATA
def create_request(pin_user_id, title, description
                   , category_id, status, created_at
                   , updated_at, view_count, location):
        try:
            cursor = db.cursor()
            sql = """
                INSERT INTO request (pin_user_id, title, description, category_id
                , status, created_at, updated_at
                , view_count, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (pin_user_id, title, description, category_id
                , status, created_at, updated_at
                , view_count, location))
            db.commit()

            id = cursor.lastrowid
            cursor.close()

            return {
                'id': id, 'pin_user_id': pin_user_id,'title': title
                ,'description': description,'status': status
                ,'created_at': created_at,'updated_at': updated_at
                ,'view_count': view_count,'category_id': category_id
                ,'location': location}
        except Exception as e:
            raise Exception(f"Error creating user: {e}")
        
def save_shortlist(csr_id: int, request_id: int, added_at: datetime) -> None:
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO shortlist (csr_user_id, request_id, added_at) VALUES (%s, %s, %s)",
                (csr_id, request_id, added_at)
            )
            db.commit()
        finally:
            cur.close()

def save_view(request_id: int, timestamp: datetime) -> None:
            cur = db.cursor()
            try:
                cur.execute(
                    "INSERT INTO request_view (request_id, viewed_at) VALUES (%s, %s)",
                    (request_id, timestamp)
                )
                db.commit()
            finally:
                cur.close()

def ensure_completed_match(
    request_id: int,
    pin_user_id: int,
    csr_user_id: int,
    service_date: datetime,
    completion_date: datetime
):

    cur3 = db.cursor()
    try:
        cur3.execute(
            """
            INSERT INTO `match`
                (request_id, csr_user_id, pin_user_id, service_date, completion_date, status)
            VALUES
                (%s, %s, %s, %s, %s, 'Completed')
            """,
            (request_id, csr_user_id, pin_user_id, service_date, completion_date),
        )  
        
        
        new_id = cur3.lastrowid
        db.commit()
        return new_id
    except Exception as e:
        print("error:", e)
    finally:
        cur3.close()


def make_title(cat_id, idx):
    # Make a descriptive title that clearly matches the category
    base = category[cat_id-1]
    return f"{base} Request #{idx:03d}"

def make_description(cat_id):
    # Short themed description by category
    theme = category[cat_id-1]
    return fake.sentence(nb_words=10) + f" Related to {theme.lower()}."
        
statuses = ['Open', 'In Progress', 'Cancelled', 'Completed']
statuses_weight = [30, 30, 10, 50]

locations = ["Orchard", "Outram Park", "Dhoby Ghaut"
             , "City Hall", "Raffles Place", "Marina Bay"
             , "Bayfront", "Bishan", "Serangoon", "Paya Lebar"
             , "Tampines", "Pasir Ris", "Changi Airport", "Jurong East"
             , "Clementi", "Buona Vista", "Holland Village", "Chinatown"
             , "Little India", "HarbourFront"]

csr_count = int(len(user_by_role['Csr_Rep'])/2)
for i in range(number_of_request_to_generate):
    percent = int((i / number_of_request_to_generate) * 100)
    steps = percent // 5
    bar = "=" * steps + " " * (20 - steps)
    sys.stdout.write("\rProgress: [%-20s] %3d%% (%d/%d)\n\n" % (bar, percent, i, number_of_request_to_generate))
    sys.stdout.flush()

    cat_id = random.randint(1,10)
    title = make_title(cat_id, i)
    description = make_description(cat_id)
    status = random.choice(statuses)
    created_at, updated_at = random_datetime_this_year(35)
    pin_id = random.choice(user_by_role['PIN_Support'])['id']
    location = random.choice(locations)
    request = create_request(pin_id, title, description
                   , cat_id, status, created_at
                   , updated_at, random.randint(1, 1000), location)
    
    # Select afew random CSR to shortlist.  Randomly choose number of CSR to save (0 to len(csr)/2)
    for csr in random.sample(user_by_role['Csr_Rep'], k = random.randint(0,csr_count)):
        save_shortlist(csr['id'], i+1, random_datetime_this_year(35)[0])
    
    for j in range(random.randint(0,100)):
        save_view(i+1, random_datetime_this_year(35)[0])

    if status == 'Completed':
        service_date, completion_date = random_datetime_this_year(35)
        ensure_completed_match(i+1, pin_id, random.choice(user_by_role['Csr_Rep'])['id'], service_date, completion_date)
    print("Created Request:", request)


db.close()