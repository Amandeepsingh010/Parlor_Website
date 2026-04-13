# 🚀 AWS DEPLOYMENT CHECKLIST - Parlor Perfect

**Version**: 2.0  
**Status**: Pre-Deployment  
**Target**: AWS EC2 + RDS

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### Step 1: Prepare AWS Environment ⬜
- [ ] AWS Account created & verified
- [ ] EC2 instance launched (Ubuntu 20.04, t2.micro or higher)
- [ ] RDS MySQL instance created
- [ ] Security groups configured
- [ ] Key pairs created & saved securely
- [ ] Elastic IP assigned (optional)

### Step 2: Update Configuration Files ⬜
- [ ] Update backend_app.py with RDS credentials:
  ```python
  db_config = {
      'host': 'your-rds-endpoint.rds.amazonaws.com',
      'user': 'admin',
      'password': 'your-strong-password',
      'database': 'dev'
  }
  ```
- [ ] Change JWT secret key in backend_app.py:
  ```python
  app.config['SECRET_KEY'] = 'generate-strong-secret-key'
  ```
- [ ] Update frontend_app.py backend URL:
  ```python
  BACKEND_API = "http://backend-private-ip:5000"
  ```
- [ ] Update social links in HTML files (Instagram, WhatsApp)
- [ ] Update business location in HTML files
- [ ] Update phone number in HTML files

### Step 3: Security Hardening ⬜
- [ ] Change MySQL admin password (minimum 16 characters)
- [ ] Generate new JWT secret key
- [ ] Update CORS origins for production
- [ ] Disable debug mode in Flask:
  ```python
  app.run(debug=False)
  ```
- [ ] Enable HTTPS/SSL in Nginx
- [ ] Configure firewall rules
- [ ] Setup AWS WAF (optional)

### Step 4: Database Setup ⬜
- [ ] Execute database_schema.sql on RDS
  ```bash
  mysql -h your-rds-endpoint -u admin -p dev < database_schema.sql
  ```
- [ ] Verify tables created:
  ```sql
  SHOW TABLES;
  ```
- [ ] Verify sample data:
  ```sql
  SELECT * FROM services LIMIT 5;
  ```
- [ ] Create database backups
- [ ] Setup RDS automated backups (7-30 days)
- [ ] Test connection from EC2 instance

### Step 5: EC2 Setup ⬜
- [ ] SSH into EC2 instance
- [ ] Update system packages:
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- [ ] Install Python 3.8+:
  ```bash
  sudo apt install python3 python3-pip python3-venv -y
  ```
- [ ] Install Git (for cloning):
  ```bash
  sudo apt install git -y
  ```
- [ ] Create project directory:
  ```bash
  sudo mkdir -p /var/www/parlor-perfect
  sudo chown ubuntu:ubuntu /var/www/parlor-perfect
  ```
- [ ] Clone/upload project files
- [ ] Create virtual environment:
  ```bash
  cd /var/www/parlor-perfect
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] Install Python dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Step 6: Nginx Installation ⬜
- [ ] Install Nginx:
  ```bash
  sudo apt install nginx -y
  ```
- [ ] Create Nginx config (see template below)
- [ ] Test Nginx:
  ```bash
  sudo nginx -t
  ```
- [ ] Enable and start Nginx:
  ```bash
  sudo systemctl enable nginx
  sudo systemctl start nginx
  ```
- [ ] Verify Nginx is running:
  ```bash
  sudo systemctl status nginx
  ```

### Step 7: SSL/TLS Certificate ⬜
- [ ] Install Certbot:
  ```bash
  sudo apt install certbot python3-certbot-nginx -y
  ```
- [ ] Generate certificate:
  ```bash
  sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com
  ```
- [ ] Update Nginx config with SSL paths
- [ ] Test SSL:
  ```bash
  sudo certbot renew --dry-run
  ```
- [ ] Enable auto-renewal:
  ```bash
  sudo systemctl enable certbot.timer
  ```

### Step 8: Systemd Services ⬜
- [ ] Create backend service file:
  ```bash
  sudo nano /etc/systemd/system/parlor-backend.service
  ```
- [ ] Create frontend service file:
  ```bash
  sudo nano /etc/systemd/system/parlor-frontend.service
  ```
- [ ] Reload systemd:
  ```bash
  sudo systemctl daemon-reload
  ```
- [ ] Enable services:
  ```bash
  sudo systemctl enable parlor-backend
  sudo systemctl enable parlor-frontend
  ```
- [ ] Start services:
  ```bash
  sudo systemctl start parlor-backend
  sudo systemctl start parlor-frontend
  ```
- [ ] Verify services:
  ```bash
  sudo systemctl status parlor-backend
  sudo systemctl status parlor-frontend
  ```

### Step 9: Monitoring & Logging ⬜
- [ ] Setup CloudWatch logs
- [ ] Configure application logs:
  ```bash
  mkdir -p /var/www/parlor-perfect/logs
  ```
- [ ] Setup log rotation:
  ```bash
  sudo nano /etc/logrotate.d/parlor-perfect
  ```
- [ ] Install monitoring tools (optional):
  ```bash
  sudo apt install htop iotop nethogs -y
  ```

### Step 10: Backup Strategy ⬜
- [ ] Enable RDS automated backups
- [ ] Setup daily database dumps to S3
- [ ] Configure backup retention (30 days minimum)
- [ ] Test restore procedure
- [ ] Document backup recovery process

### Step 11: Final Testing ⬜
- [ ] Test frontend access: https://your-domain.com
- [ ] Test backend API: https://your-domain.com/api/services
- [ ] Test login with admin account
- [ ] Test service creation/editing/deletion
- [ ] Test booking functionality
- [ ] Test discount management
- [ ] Test animations load properly
- [ ] Test mobile responsiveness
- [ ] Test email notifications (if implemented)
- [ ] Load testing with Apache Bench

### Step 12: Go Live ⬜
- [ ] Update DNS records to point to Elastic IP
- [ ] Verify DNS propagation (can take 24-48 hours)
- [ ] Test with domain name instead of IP
- [ ] Announce to customers
- [ ] Monitor logs for errors
- [ ] Track performance metrics

### Step 13: Post-Deployment ⬜
- [ ] Document deployment procedure
- [ ] Create runbook for common issues
- [ ] Setup alerting for errors
- [ ] Train team on admin panel
- [ ] Setup disaster recovery plan
- [ ] Schedule regular security updates

---

## 🔧 CONFIGURATION TEMPLATES

### Nginx Configuration
```nginx
# /etc/nginx/sites-available/parlor-perfect

upstream backend {
    server 127.0.0.1:5000;
}

upstream frontend {
    server 127.0.0.1:81;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_types text/css text/javascript application/json;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

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

    # Static Files
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Deny Access to Sensitive Files
    location ~ /\. {
        deny all;
    }
}
```

### Backend Systemd Service
```ini
# /etc/systemd/system/parlor-backend.service

[Unit]
Description=Parlor Perfect Backend API Server
After=network.target mysql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/parlor-perfect
Environment="PATH=/var/www/parlor-perfect/venv/bin"
ExecStart=/var/www/parlor-perfect/venv/bin/python backend_app.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Frontend Systemd Service
```ini
# /etc/systemd/system/parlor-frontend.service

[Unit]
Description=Parlor Perfect Frontend Web Server
After=network.target parlor-backend.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/parlor-perfect
Environment="PATH=/var/www/parlor-perfect/venv/bin"
ExecStart=/var/www/parlor-perfect/venv/bin/python frontend_app.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Firewall Rules
```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS
sudo ufw allow 443/tcp

# Deny everything else
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Enable firewall
sudo ufw enable

# Verify rules
sudo ufw status
```

---

## 🔍 POST-DEPLOYMENT VERIFICATION

### Test Commands
```bash
# Test frontend
curl -I https://your-domain.com
curl https://your-domain.com | grep "Parlor Perfect"

# Test backend
curl https://your-domain.com/api/services
curl https://your-domain.com/api/festival-discount

# Test SSL
openssl s_client -connect your-domain.com:443 -tls1_2

# Check service status
sudo systemctl status parlor-backend
sudo systemctl status parlor-frontend
sudo systemctl status nginx

# Monitor logs
sudo journalctl -u parlor-backend -f
sudo journalctl -u parlor-frontend -f

# Check disk space
df -h

# Check memory
free -h

# Check CPU usage
top -bn1 | head -n 15
```

---

## 🚨 TROUBLESHOOTING DEPLOYMENT

### Cannot Connect to RDS
```bash
# Check security group
# Ensure RDS security group allows port 3306 from EC2 SG

# Test connection
mysql -h your-rds-endpoint -u admin -p -e "SELECT 1"

# Check credentials in backend_app.py
```

### Services Not Starting
```bash
# Check logs
sudo journalctl -u parlor-backend -n 50

# Check syntax
python -m py_compile backend_app.py

# Check port availability
sudo lsof -i :5000
sudo lsof -i :81
```

### Nginx Not Forwarding Requests
```bash
# Test Nginx config
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Restart Nginx
sudo systemctl restart nginx
```

### SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Check renewal log
sudo cat /var/log/letsencrypt/letsencrypt.log | tail -20
```

---

## 📊 MONITORING DASHBOARD

### Key Metrics to Monitor
- [ ] Backend CPU usage
- [ ] Backend Memory usage
- [ ] Database connections
- [ ] API response time
- [ ] Error rate
- [ ] Uptime percentage
- [ ] Disk space usage
- [ ] SSL certificate expiration

### Recommended Tools
- AWS CloudWatch
- New Relic
- Datadog
- Prometheus + Grafana

---

## 📞 PRODUCTION CONTACTS

**Emergency Contacts:**
- DevOps Lead: [Contact Info]
- Database Admin: [Contact Info]
- Security Team: [Contact Info]

**Escalation Procedure:**
1. Check error logs
2. Contact DevOps Lead
3. Prepare incident report
4. Execute recovery procedure

---

## ✅ SIGN-OFF

- [ ] Project Lead Approved
- [ ] Security Review Passed
- [ ] Load Testing Passed
- [ ] Final User Acceptance Test
- [ ] Go-Live Approved

**Approved By**: ________________  
**Date**: ________________

---

**Deployment Checklist v2.0**  
**Parlor Perfect - Production Deployment**

*Keep this checklist updated and handy!*
