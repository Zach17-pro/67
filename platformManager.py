from app import db
from flask import jsonify, request
from app import app

# ---------------------------
# Platform Manager API routes
# ---------------------------

# Read all service categories
@app.route('/platform_manager/api/read', methods=['GET'])
def pm_read_categories():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT category_id as id, category_name as name FROM service_categories")  # FIXED
        categories = cursor.fetchall()
        cursor.close()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add a new category
@app.route('/platform_manager/api/create', methods=['POST'])
def pm_create_category():
    try:
        data = request.get_json()
        name = data.get('category_name')

        if not name:
            return jsonify({'error': 'Category name is required'}), 400

        cursor = db.cursor()
        cursor.execute("INSERT INTO service_categories (category_name) VALUES (%s)", (name,))  # FIXED
        db.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return jsonify({'success': True, 'id': last_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a category
@app.route('/platform_manager/api/update', methods=['PUT'])
def pm_update_category():
    try:
        data = request.get_json()
        category_id = data.get('id')
        name = data.get('category_name')

        if not category_id or not name:
            return jsonify({'error': 'Category ID and name are required'}), 400

        cursor = db.cursor()
        cursor.execute("UPDATE service_categories SET category_name=%s WHERE category_id=%s", (name, category_id))  # FIXED
        db.commit()
        cursor.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a category
@app.route('/platform_manager/api/delete', methods=['DELETE'])
def pm_delete_category():
    try:
        data = request.get_json()
        category_id = data.get('id')

        if not category_id:
            return jsonify({'error': 'Category ID is required'}), 400

        cursor = db.cursor()
        cursor.execute("DELETE FROM service_categories WHERE category_id=%s", (category_id,))  # FIXED
        db.commit()
        cursor.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500