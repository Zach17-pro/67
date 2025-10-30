from flask import Blueprint, current_app

health_api = Blueprint("health", __name__)

@health_api.get("/test_db")
def test_db():
    try:
        db = current_app.config["DB"]
        cur = db.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        return f"Database connection successful! Test query result: {result}"
    except Exception as e:
        return f"Database connection failed: {str(e)}"
