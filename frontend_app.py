from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import requests
import json
from functools import wraps

app = Flask(__name__)
CORS(app)
app.secret_key = "your-secret-key-change-in-production"

# Backend API Configuration
BACKEND_API = "http://127.0.0.1:5000"  # Change to your backend private IP on AWS

# ==================== MIDDLEWARE ====================

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('auth_page'))
        
        # Verify token is still valid
        try:
            response = requests.get(
                f"{BACKEND_API}/auth/verify",
                headers={'Authorization': f'Bearer {session["token"]}'}
            )
            if response.status_code != 200:
                session.clear()
                return redirect(url_for('auth_page'))
        except Exception as e:
            session.clear()
            return redirect(url_for('auth_page'))
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin' not in session or not session['is_admin']:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTH ROUTES ====================

@app.route('/auth', methods=['GET', 'POST'])
def auth_page():
    """Auth page for login/register"""
    if request.method == 'POST':
        return handle_auth()
    return render_template('auth.html')

def handle_auth():
    """Handle login/register AJAX requests"""
    data = request.json
    action = data.get('action')  # 'login' or 'register'
    
    try:
        if action == 'register':
            response = requests.post(
                f"{BACKEND_API}/auth/register",
                json={
                    'name': data.get('name'),
                    'email': data.get('email'),
                    'phone': data.get('phone'),
                    'password': data.get('password')
                }
            )
        elif action == 'login':
            response = requests.post(
                f"{BACKEND_API}/auth/login",
                json={
                    'email': data.get('email'),
                    'password': data.get('password')
                }
            )
        else:
            return jsonify({'error': 'Invalid action'}), 400
        
        if response.status_code in [200, 201]:
            resp_data = response.json()
            session['token'] = resp_data['token']
            session['user_id'] = resp_data['user_id']
            session['name'] = resp_data.get('name', 'User')
            session['is_admin'] = resp_data.get('is_admin', 0)
            
            redirect_url = url_for('admin_dashboard') if session['is_admin'] else url_for('customer_home')
            return jsonify({'success': True, 'redirect': redirect_url}), 200
        else:
            error_msg = response.json().get('error', 'Authentication failed')
            return jsonify({'success': False, 'error': error_msg}), response.status_code
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/logout', methods=['GET'])
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('auth_page'))

# ==================== CUSTOMER ROUTES ====================

@app.route('/', methods=['GET'])
@login_required
def customer_home():
    """Customer home page"""
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    
    try:
        # Fetch services
        services_resp = requests.get(f"{BACKEND_API}/services")
        services = services_resp.json() if services_resp.status_code == 200 else {}
        
        # Fetch festival discount
        discount_resp = requests.get(f"{BACKEND_API}/festival-discount")
        festival_discount = discount_resp.json() if discount_resp.status_code == 200 else {}
        
        return render_template(
            'customer/home.html',
            services=services,
            festival_discount=festival_discount,
            user_name=session.get('name')
        )
    except Exception as e:
        return render_template('customer/home.html', services={}, error=str(e))

@app.route('/services', methods=['GET'])
@login_required
def customer_services():
    """Customer services page"""
    try:
        response = requests.get(f"{BACKEND_API}/services")
        services = response.json() if response.status_code == 200 else {}
        
        discount_resp = requests.get(f"{BACKEND_API}/festival-discount")
        festival_discount = discount_resp.json() if discount_resp.status_code == 200 else {}
        
        return render_template(
            'customer/services.html',
            services=services,
            festival_discount=festival_discount
        )
    except Exception as e:
        return render_template('customer/services.html', services={}, error=str(e))

@app.route('/bookings', methods=['GET'])
@login_required
def customer_bookings():
    """Customer bookings page"""
    try:
        response = requests.get(
            f"{BACKEND_API}/bookings",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        bookings = response.json() if response.status_code == 200 else []
        return render_template('customer/bookings.html', bookings=bookings)
    except Exception as e:
        return render_template('customer/bookings.html', bookings=[], error=str(e))

@app.route('/profile', methods=['GET'])
@login_required
def customer_profile():
    """Customer profile page"""
    try:
        response = requests.get(
            f"{BACKEND_API}/users/{session['user_id']}",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        user = response.json() if response.status_code == 200 else {}
        return render_template('customer/profile.html', user=user)
    except Exception as e:
        return render_template('customer/profile.html', user={}, error=str(e))

# ==================== ADMIN ROUTES ====================

@app.route('/admin', methods=['GET'])
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    try:
        services_resp = requests.get(
            f"{BACKEND_API}/services",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        services = services_resp.json() if services_resp.status_code == 200 else {}
        
        return render_template('admin/dashboard.html', services=services)
    except Exception as e:
        return render_template('admin/dashboard.html', services={}, error=str(e))

@app.route('/admin/services', methods=['GET'])
@login_required
@admin_required
def admin_services():
    """Admin services management"""
    try:
        response = requests.get(
            f"{BACKEND_API}/services",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        services = response.json() if response.status_code == 200 else {}
        return render_template('admin/services.html', services=services)
    except Exception as e:
        return render_template('admin/services.html', services={}, error=str(e))

@app.route('/admin/discount', methods=['GET'])
@login_required
@admin_required
def admin_discount():
    """Admin festival discount management"""
    try:
        response = requests.get(
            f"{BACKEND_API}/festival-discount",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        discount = response.json() if response.status_code == 200 else {}
        return render_template('admin/discount.html', discount=discount)
    except Exception as e:
        return render_template('admin/discount.html', discount={}, error=str(e))

@app.route('/admin/bookings', methods=['GET'])
@login_required
@admin_required
def admin_bookings():
    """Admin bookings management"""
    try:
        response = requests.get(
            f"{BACKEND_API}/bookings",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        bookings = response.json() if response.status_code == 200 else []
        return render_template('admin/bookings.html', bookings=bookings)
    except Exception as e:
        return render_template('admin/bookings.html', bookings=[], error=str(e))

@app.route('/admin/users', methods=['GET'])
@login_required
@admin_required
def admin_users():
    """Admin users management"""
    try:
        response = requests.get(
            f"{BACKEND_API}/users",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        users = response.json() if response.status_code == 200 else []
        return render_template('admin/users.html', users=users)
    except Exception as e:
        return render_template('admin/users.html', users=[], error=str(e))

# ==================== API PROXY ROUTES ====================

@app.route('/api/services', methods=['GET'])
@login_required
def api_get_services():
    """Proxy: Get services"""
    try:
        response = requests.get(
            f"{BACKEND_API}/services",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/services', methods=['POST'])
@login_required
@admin_required
def api_add_service():
    """Proxy: Add service"""
    try:
        response = requests.post(
            f"{BACKEND_API}/services",
            json=request.json,
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/services/<int:service_id>', methods=['PUT'])
@login_required
@admin_required
def api_update_service(service_id):
    """Proxy: Update service"""
    try:
        response = requests.put(
            f"{BACKEND_API}/services/{service_id}",
            json=request.json,
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/services/<int:service_id>', methods=['DELETE'])
@login_required
@admin_required
def api_delete_service(service_id):
    """Proxy: Delete service"""
    try:
        response = requests.delete(
            f"{BACKEND_API}/services/{service_id}",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/festival-discount', methods=['GET'])
def api_get_discount():
    """Proxy: Get festival discount"""
    try:
        response = requests.get(f"{BACKEND_API}/festival-discount")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/festival-discount', methods=['PUT'])
@login_required
@admin_required
def api_update_discount():
    """Proxy: Update festival discount"""
    try:
        response = requests.put(
            f"{BACKEND_API}/festival-discount",
            json=request.json,
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings', methods=['GET'])
@login_required
def api_get_bookings():
    """Proxy: Get bookings"""
    try:
        response = requests.get(
            f"{BACKEND_API}/bookings",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings', methods=['POST'])
@login_required
def api_add_booking():
    """Proxy: Add booking"""
    try:
        response = requests.post(
            f"{BACKEND_API}/bookings",
            json=request.json,
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
@login_required
def api_delete_booking(booking_id):
    """Proxy: Delete booking"""
    try:
        response = requests.delete(
            f"{BACKEND_API}/bookings/{booking_id}",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET'])
@login_required
def api_get_profile():
    """Proxy: Get user profile"""
    try:
        response = requests.get(
            f"{BACKEND_API}/users/{session['user_id']}",
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['PUT'])
@login_required
def api_update_profile():
    """Proxy: Update user profile"""
    try:
        response = requests.put(
            f"{BACKEND_API}/users/{session['user_id']}",
            json=request.json,
            headers={'Authorization': f'Bearer {session["token"]}'}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
