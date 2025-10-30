from typing import List, Dict, Any, Optional
from entity.service_category import ServiceCategory

class ServiceCategoryRepository:
    def __init__(self, db):
        self.db = db

    def list_categories(self) -> List[Dict[str, Any]]:
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT category_id AS id, category_name AS name FROM service_category")
        rows = cur.fetchall()
        cur.close()
        categories = [ServiceCategory(id=row["id"], name=row["name"]) for row in rows]
        return categories

    def create_category(self, name: str) -> int:
        cur = self.db.cursor()
        cur.execute("INSERT INTO service_category (category_name) VALUES (%s)", (name,))
        self.db.commit()
        new_id = cur.lastrowid
        cur.close()
        return ServiceCategory(id=new_id, name=name)

    def update_category(self, category_id: int, name: str) -> None:
        cur = self.db.cursor()
        cur.execute("UPDATE service_category SET category_name = %s WHERE category_id = %s", (name, category_id))
        self.db.commit()
        cur.close()
        return ServiceCategory(id=category_id, name=name)
        

    def delete_category(self, category_id: int) -> None:
        cur = self.db.cursor()
        cur.execute("DELETE FROM service_category WHERE category_id = %s", (category_id,))
        self.db.commit()
        cur.close()
        return ServiceCategory(id=category_id, name=None)
