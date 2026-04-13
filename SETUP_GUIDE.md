# Parlor Perfect - Beauty Management System
## Complete Setup Guide

---

## Project Overview

Parlor Perfect is a comprehensive beauty parlor management system built with:
- **Frontend**: Flask + HTML5 + CSS3 + JavaScript (GSAP + Anime.js animations)
- **Backend**: Flask + Python with JWT Authentication
- **Database**: MySQL (AWS RDS)
- **Hosting**: AWS EC2
- **Animation Libraries**: GSAP 3.12.2, Anime.js 3.2.1

### Features:
✨ User Authentication (Login/Register with JWT)
💇 Dynamic Service Management (Facials, Nails, Waxing, Threading, etc.)
💰 Festival Discount Management
📅 Booking System
👩‍💼 Admin Dashboard with Full CRUD Operations
🎨 Beautiful Baby Pink Theme with Smooth Animations
📱 Fully Responsive Design
🔐 Secure JWT Token-based Authentication

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Client Browser                        │
│              (HTML5 + CSS3 + JavaScript)               │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/HTTPS
┌──────────────────▼──────────────────────────────────────┐
│              Frontend Server (Port 81)                  │
│           Flask Application + Jinja2 Templates          │
│              (Authentication Middleware)                │
└──────────────────┬──────────────────────────────────────┘
                   │ Requests
┌──────────────────▼──────────────────────────────────────┐
│              Backend Server (Port 5000)                 │
│        Flask API + JWT Token Verification               │
│              (CORS Enabled for Dev)                     │
└──────────────────┬──────────────────────────────────────┘
                   │ mysql.connector
┌──────────────────▼──────────────────────────────────────┐
│                AWS RDS MySQL Database                   │
│          (book-rds.cinsoscgioqa.us-east-1)            │
└──────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### System Requirements:
- Ubuntu 20.04+ or Amazon Linux 2
- Python 3.8+
- MySQL 8.0+
- 2GB RAM minimum
- 10GB Storage

### Required Python Packages:
```
Flask==2.3.0
Flask-CORS==4.0.0
mysql-connector-python==8.0.33
PyJWT==2.8.0
requests==2.31.0
Werkzeug==2.3.0
```

---

## Installation & Setup

### Step 1: Install Python & Dependencies

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install required system packages
sudo apt install git curl wget -y
```

### Step 2: Clone/Setup Project Structure

```bash
# Create project directory
mkdir -p /var/www/parlor-perfect
cd /var/www/parlor-perfect

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Create directory structure
mkdir -p frontend backend templates/admin templates/customer static logs
```

### Step 3: Install Python Dependencies

```bash
# Create requirements.txt
cat > requirements.txt << EOF
Flask==2.3.0
Flask-CORS==4.0.0
mysql-connector-python==8.0.33
PyJWT==2.8.0
requests==2.31.0
Werkzeug==2.3.0
EOF

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Database Setup

```bash
# Connect to MySQL (on your RDS or local MySQL)
mysql -h book-rds.cinsoscgioqa.us-east-1.rds.amazonaws.com -u admin -p

# Run the schema script (database_schema.sql content)
# Copy the entire SQL from database_schema.sql and paste into MySQL

# Or if you have the file:
mysql -h book-rds.cinsoscgioqa.us-east-1.rds.amazonaws.com -u admin -p dev < database_schema.sql
```

### Step 5: Configure Backend Server

```bash
# Create backend configuration file
cat > backend_config.py << 'EOF'
# Backend Configuration
DATABASE = {
    'host': 'book-rds.cinsoscgioqa.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'SuperSecretPass123',
    'database': 'dev'
}

JWT_CONFIG = {
    'secret_key': 'your-secret-key-change-in-production',
    'algorithm': 'HS256',
    'expiration': 24  # hours
}

BACKEND_PORT = 5000
BACKEND_HOST = '0.0.0.0'
EOF
```

### Step 6: Configure Frontend Server

```bash
# Update backend API URL in frontend_app.py
# Change:
# BACKEND_API = "http://127.0.0.1:5000"
# To your backend server IP (for AWS):
# BACKEND_API = "http://backend-private-ip:5000"
```

### Step 7: Create Systemd Services

#### Backend Service

```bash
sudo tee /etc/systemd/system/parlor-backend.service > /dev/null << 'EOF'
[Unit]
Description=Parlor Perfect Backend Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/parlor-perfect
Environment="PATH=/var/www/parlor-perfect/venv/bin"
ExecStart=/var/www/parlor-perfect/venv/bin/python backend_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable parlor-backend.service
sudo systemctl start parlor-backend.service
```

#### Frontend Service

```bash
sudo tee /etc/systemd/system/parlor-frontend.service > /dev/null << 'EOF'
[Unit]
Description=Parlor Perfect Frontend Server
After=network.target parlor-backend.service

[Service]
User=ubuntu
WorkingDirectory=/var/www/parlor-perfect
Environment="PATH=/var/www/parlor-perfect/venv/bin"
ExecStart=/var/www/parlor-perfect/venv/bin/python frontend_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable parlor-frontend.service
sudo systemctl start parlor-frontend.service
```

### Step 8: Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/parlor-perfect > /dev/null << 'EOF'
# Backend API Server
upstream backend {
    server 127.0.0.1:5000;
}

# Frontend Application Server
upstream frontend {
    server 127.0.0.1:81;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/parlor-perfect /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### Step 9: Setup SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generate SSL certificate
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Step 10: Verify Installation

```bash
# Check backend service
sudo systemctl status parlor-backend.service

# Check frontend service
sudo systemctl status parlor-frontend.service

# Check Nginx
sudo systemctl status nginx

# View logs
tail -f /var/www/parlor-perfect/venv/logs/backend.log
tail -f /var/www/parlor-perfect/venv/logs/frontend.log
```

---

## Configuration Files

### backend_app.py Configuration

```python
# Change these in production:
app.config['SECRET_KEY'] = 'your-very-secret-key-change-this'

db_config = {
    'host': 'your-rds-endpoint',
    'user': 'your-db-user',
    'password': 'your-db-password',
    'database': 'your-database'
}
```

### frontend_app.py Configuration

```python
app.secret_key = "your-secret-key-change-in-production"
BACKEND_API = "http://backend-ip:5000"  # Update for production
```

---

## File Structure

```
/var/www/parlor-perfect/
├── backend_app.py                 # Backend API server
├── frontend_app.py                # Frontend Flask app
├── database_schema.sql            # Database initialization
├── requirements.txt               # Python dependencies
├── venv/                          # Virtual environment
├── templates/
│   ├── auth.html                 # Login/Register page
│   ├── customer/
│   │   ├── home.html            # Customer dashboard
│   │   ├── services.html        # Services listing
│   │   ├── bookings.html        # User bookings
│   │   └── profile.html         # User profile
│   └── admin/
│       ├── dashboard.html       # Admin panel
│       ├── services.html        # Service management
│       ├── discount.html        # Discount management
│       ├── bookings.html        # Booking management
│       └── users.html           # User management
├── static/
│   ├── css/                      # CSS files
│   ├── js/                       # JavaScript files
│   └── images/                   # Images
└── logs/                         # Application logs
```

---

## API Endpoints Reference

### Authentication
```
POST   /auth/register              - Register new user
POST   /auth/login                 - Login user
GET    /auth/verify                - Verify JWT token
```

### Services
```
GET    /services                   - Get all services
POST   /services                   - Add service (admin)
PUT    /services/<id>              - Update service (admin)
DELETE /services/<id>              - Delete service (admin)
```

### Festival Discount
```
GET    /festival-discount          - Get current discount
PUT    /festival-discount          - Update discount (admin)
```

### Bookings
```
GET    /bookings                   - Get bookings
POST   /bookings                   - Create booking
DELETE /bookings/<id>              - Cancel booking
```

### Users
```
GET    /users                      - Get all users (admin)
GET    /users/<id>                 - Get user profile
PUT    /users/<id>                 - Update profile
DELETE /users/<id>                 - Delete user (admin)
```

---

## Default Credentials

### Admin User
- **Email**: admin@parlor.com
- **Password**: admin123 (hashed in DB)

---

## Troubleshooting

### Backend won't start
```bash
# Check for port conflicts
sudo lsof -i :5000

# Check error logs
journalctl -u parlor-backend.service -n 50
```

### Database connection error
```bash
# Test MySQL connection
mysql -h book-rds.cinsoscgioqa.us-east-1.rds.amazonaws.com -u admin -p -e "SELECT 1"

# Check credentials in backend_app.py
```

### CORS errors
```bash
# Ensure CORS is enabled in backend_app.py
from flask_cors import CORS
CORS(app)
```

### JWT token expired
```bash
# Clear browser cookies and login again
# Token expiration is set to 24 hours by default
```

---

## Security Recommendations

1. **Change default credentials** immediately
2. **Use strong database password** (minimum 16 characters)
3. **Enable SSL/TLS** (Let's Encrypt - already in setup)
4. **Update JWT secret key** in production
5. **Setup firewall rules**:
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```
6. **Regular backups** of database
7. **Monitor logs** regularly

---

## Performance Optimization

1. **Enable gzip compression** in Nginx
2. **Use Redis** for session caching
3. **Optimize images** in static folder
4. **Enable CDN** for static assets
5. **Database indexing** (already in schema)

---

## Monitoring & Logs

```bash
# View all application logs
tail -f /var/log/syslog | grep parlor

# Monitor resource usage
top

# Check disk space
df -h

# Monitor database
mysql -h book-rds.cinsoscgioqa.us-east-1.rds.amazonaws.com -u admin -p
```

---

## Support & Maintenance

- **Regular Updates**: Update Python packages monthly
- **Database Maintenance**: Run optimization queries
- **Security Patches**: Apply patches immediately
- **Backup Strategy**: Daily automated backups to S3

---

## Contact Information

For the parlor business:
- **Phone**: +91 98765 43210
- **WhatsApp**: https://wa.me/919876543210
- **Instagram**: https://www.instagram.com/parlor.perfect
- **Location**: 123 Beauty Lane, Hyderabad, Telangana 500001

---

## License & Credits

Built with ❤️ for beauty professionals
© 2024 Parlor Perfect. All rights reserved.

**Technologies Used:**
- Flask 2.3
- MySQL 8.0
- JWT Authentication
- GSAP 3.12.2 (Animations)
- Anime.js 3.2.1 (Animations)
- Nginx (Web Server)
- AWS RDS (Database)
- AWS EC2 (Hosting)
