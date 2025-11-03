from app import db
from flask import jsonify, request, session, flash, redirect, url_for
from app import app


###########################
###### USER ACCOUNTS ######
###########################

# Admin API routes
@app.route('/api/admin', methods=['POST'])
def admin_create_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO user (username, password, role, full_name) VALUES (%s, %s, %s, %s)", 
                      (username, password, role, username))
        db.commit()
        cursor.close()
        return jsonify({'success': True, 'id': cursor.lastrowid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin', methods=['GET'])
def admin_read_users():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT user_id as id, username, role FROM user")
        users = cursor.fetchall()
        cursor.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin', methods=['PUT'])
def admin_update_user():
    try:
        data = request.get_json()
        user_id = data.get('id')
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        
        if password:  # Only update password if provided
            cursor = db.cursor()
            cursor.execute("UPDATE user SET username = %s, password = %s, role = %s WHERE user_id = %s", 
                          (username, password, role, user_id))
        else:  # Keep current password if not provided
            cursor = db.cursor()
            cursor.execute("UPDATE user SET username = %s, role = %s WHERE user_id = %s", 
                          (username, role, user_id))
        db.commit()
        cursor.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin', methods=['DELETE'])
def admin_delete_user():
    try:
        data = request.get_json()
        user_id = data.get('id')
        
        cursor = db.cursor()
        cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
        db.commit()
        cursor.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


###########################
###### USER PROFILES ######
###########################

@app.route('/api/admin/profile', methods=['POST'])
def admin_create_profile():
    try:
        data = request.get_json()
        username = data.get('username')
        full_name = data.get('full_name')
        email = data.get('email')

        if not username or not full_name:
            return jsonify({'error': 'Username and Full Name are required'}), 400

        # Default password if none provided
        default_password = 'default123'  

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO user (username, full_name, email, password)
            VALUES (%s, %s, %s, %s)
        """, (username, full_name, email, default_password))
        db.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({'success': True, 'id': new_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/profile', methods=['GET'])
def admin_read_profiles():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT user_id as id, username, full_name, email FROM user")
        profiles = cursor.fetchall()
        cursor.close()
        return jsonify(profiles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/profile', methods=['PUT'])
def admin_update_profile():
    try:
        data = request.get_json()
        user_id = data.get('id')
        full_name = data.get('full_name')
        email = data.get('email')
        
        cursor = db.cursor()
        cursor.execute("UPDATE user SET full_name = %s, email = %s WHERE user_id = %s", 
                      (full_name, email, user_id))
        db.commit()
        cursor.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/api/admin/profile', methods=['DELETE'])
def admin_delete_profile():
    """#10 As a user admin, I want to delete user profiles so that invalid records are removed."""
    try:
        data = request.get_json()
        user_id = data.get('id')

        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        cursor = db.cursor()
        cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
        db.commit()
        cursor.close()
        return jsonify({'success': True, 'deleted_user_id': user_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    