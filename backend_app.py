from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, timedelta
import jwt
import hashlib
import json
from functools import wraps

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION = 24  # hours

# Database Configuration
db_config = {
    'host': 'book-rds.cinsoscgioqa.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'SuperSecretPass123',
    'database': 'dev'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# ==================== AUTHENTICATION ====================

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_jwt_token(user_id, is_admin):
    """Create JWT token"""
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm=JWT_ALGORITHM)
    return token

def token_required(f):
    """Decorator to verify JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Missing token'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[JWT_ALGORITHM])
            request.user_id = data['user_id']
            request.is_admin = data['is_admin']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

# ==================== AUTH ENDPOINTS ====================

@app.route('/auth/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone', '')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({'error': 'Name, Email, and Password are required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed_pwd = hash_password(password)
        cursor.execute(
            """INSERT INTO users (name, email, phone, password, is_admin, created_at) 
               VALUES (%s, %s, %s, %s, 0, %s)""",
            (name, email, phone, hashed_pwd, datetime.now())
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        token = create_jwt_token(user_id, 0)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user_id': user_id,
            'is_admin': 0
        }), 201
    except mysql.connector.Error as err:
        if "Duplicate" in str(err):
            return jsonify({'error': 'Email already registered'}), 409
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and Password are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, password, is_admin, name FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        hashed_pwd = hash_password(password)
        if user['password'] != hashed_pwd:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        token = create_jwt_token(user['id'], user['is_admin'])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user_id': user['id'],
            'name': user['name'],
            'is_admin': user['is_admin']
        }), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/auth/verify', methods=['GET'])
@token_required
def verify_token():
    """Verify JWT token"""
    return jsonify({
        'valid': True,
        'user_id': request.user_id,
        'is_admin': request.is_admin
    }), 200

# ==================== USERS ENDPOINTS ====================

@app.route('/users', methods=['GET'])
@token_required
@admin_required
def get_users():
    """Get all users (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, phone, is_admin, created_at FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """Get user profile"""
    if request.user_id != user_id and not request.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, phone, is_admin, created_at FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """Update user profile"""
    if request.user_id != user_id and not request.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    
    if not name or not email:
        return jsonify({'error': 'Name and Email are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'User not found'}), 404
        
        cursor.execute(
            "UPDATE users SET name = %s, email = %s, phone = %s WHERE id = %s",
            (name, email, phone, user_id)
        )
        conn.commit()
        return jsonify({'message': 'User updated successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(user_id):
    """Delete user (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'User not found'}), 404
        
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return jsonify({'message': 'User deleted successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== SERVICES/PACKAGES ENDPOINTS ====================

@app.route('/services', methods=['GET'])
def get_services():
    """Get all services grouped by category"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, category, service_name, description, base_price, 
               discount_percent, discounted_price, is_active 
        FROM services 
        WHERE is_active = 1
        ORDER BY category, service_name
    """)
    services = cursor.fetchall()
    cursor.close()
    conn.close()
    
    grouped = {}
    for service in services:
        cat = service['category']
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(service)
    
    return jsonify(grouped)

@app.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """Get single service"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM services WHERE id = %s", (service_id,))
    service = cursor.fetchone()
    cursor.close()
    conn.close()
    if service:
        return jsonify(service)
    return jsonify({'error': 'Service not found'}), 404

@app.route('/services', methods=['POST'])
@token_required
@admin_required
def add_service():
    """Add new service (admin only)"""
    data = request.json
    category = data.get('category')
    service_name = data.get('service_name')
    description = data.get('description', '')
    base_price = data.get('base_price')
    discount_percent = data.get('discount_percent', 0)
    
    if not category or not service_name or base_price is None:
        return jsonify({'error': 'Category, Service Name, and Price are required'}), 400
    
    discounted_price = float(base_price) * (1 - float(discount_percent) / 100)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO services 
               (category, service_name, description, base_price, discount_percent, discounted_price, is_active, created_at) 
               VALUES (%s, %s, %s, %s, %s, %s, 1, %s)""",
            (category, service_name, description, base_price, discount_percent, discounted_price, datetime.now())
        )
        conn.commit()
        service_id = cursor.lastrowid
        return jsonify({'message': 'Service added successfully', 'service_id': service_id}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/services/<int:service_id>', methods=['PUT'])
@token_required
@admin_required
def update_service(service_id):
    """Update service (admin only)"""
    data = request.json
    service_name = data.get('service_name')
    description = data.get('description')
    base_price = data.get('base_price')
    discount_percent = data.get('discount_percent')
    is_active = data.get('is_active', 1)
    
    if not service_name or base_price is None or discount_percent is None:
        return jsonify({'error': 'Required fields missing'}), 400
    
    discounted_price = float(base_price) * (1 - float(discount_percent) / 100)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM services WHERE id = %s", (service_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Service not found'}), 404
        
        cursor.execute(
            """UPDATE services 
               SET service_name = %s, description = %s, base_price = %s, 
                   discount_percent = %s, discounted_price = %s, is_active = %s
               WHERE id = %s""",
            (service_name, description, base_price, discount_percent, discounted_price, is_active, service_id)
        )
        conn.commit()
        return jsonify({'message': 'Service updated successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/services/<int:service_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_service(service_id):
    """Delete service (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM services WHERE id = %s", (service_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Service not found'}), 404
        
        cursor.execute("DELETE FROM services WHERE id = %s", (service_id,))
        conn.commit()
        return jsonify({'message': 'Service deleted successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== FESTIVAL DISCOUNT ENDPOINTS ====================

@app.route('/festival-discount', methods=['GET'])
def get_festival_discount():
    """Get current festival discount"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, discount_percent, description, is_active, created_at, updated_at 
        FROM festival_discount 
        WHERE is_active = 1 
        ORDER BY updated_at DESC 
        LIMIT 1
    """)
    discount = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if discount:
        return jsonify(discount)
    return jsonify({'discount_percent': 0, 'description': 'No active discount', 'is_active': 0}), 200

@app.route('/festival-discount', methods=['PUT'])
@token_required
@admin_required
def update_festival_discount():
    """Update festival discount (admin only)"""
    data = request.json
    discount_percent = data.get('discount_percent', 0)
    description = data.get('description', '')
    is_active = data.get('is_active', 1)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM festival_discount LIMIT 1")
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute(
                """UPDATE festival_discount 
                   SET discount_percent = %s, description = %s, is_active = %s, updated_at = %s""",
                (discount_percent, description, is_active, datetime.now())
            )
        else:
            cursor.execute(
                """INSERT INTO festival_discount (discount_percent, description, is_active, created_at, updated_at) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (discount_percent, description, is_active, datetime.now(), datetime.now())
            )
        
        conn.commit()
        return jsonify({'message': 'Festival discount updated successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== BOOKINGS ENDPOINTS ====================

@app.route('/bookings', methods=['GET'])
@token_required
def get_bookings():
    """Get bookings (user gets own, admin gets all)"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.is_admin:
        cursor.execute("""
            SELECT b.*, u.name, u.email, u.phone, s.service_name 
            FROM bookings b 
            LEFT JOIN users u ON b.user_id = u.id 
            LEFT JOIN services s ON b.service_id = s.id
            ORDER BY b.booking_date DESC
        """)
    else:
        cursor.execute("""
            SELECT b.*, u.name, u.email, u.phone, s.service_name 
            FROM bookings b 
            LEFT JOIN users u ON b.user_id = u.id 
            LEFT JOIN services s ON b.service_id = s.id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """, (request.user_id,))
    
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(bookings)

@app.route('/bookings', methods=['POST'])
@token_required
def add_booking():
    """Add new booking"""
    data = request.json
    user_id = data.get('user_id', request.user_id)
    service_id = data.get('service_id')
    booking_date = data.get('booking_date')
    notes = data.get('notes', '')
    
    if not service_id or not booking_date:
        return jsonify({'error': 'Service and Booking Date are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO bookings (user_id, service_id, booking_date, notes, status, created_at) 
               VALUES (%s, %s, %s, %s, 'pending', %s)""",
            (user_id, service_id, booking_date, notes, datetime.now())
        )
        conn.commit()
        booking_id = cursor.lastrowid
        return jsonify({'message': 'Booking created successfully', 'booking_id': booking_id}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
@token_required
def delete_booking(booking_id):
    """Delete booking"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT user_id FROM bookings WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()
        
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        if booking['user_id'] != request.user_id and not request.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        conn.commit()
        return jsonify({'message': 'Booking deleted successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== HEALTH CHECK ====================

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'Parlor Backend API Running', 'version': '2.0', 'auth': 'JWT'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
