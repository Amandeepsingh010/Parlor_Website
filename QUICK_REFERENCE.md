# ⚡ QUICK REFERENCE CARD - Parlor Perfect

## 🚀 START IN 1 MINUTE

### Installation
```bash
pip install -r requirements.txt
mysql -u root -p < database_schema.sql
python backend_app.py      # Terminal 1, Port 5000
python frontend_app.py     # Terminal 2, Port 81
```

### Access
```
Frontend: http://localhost:81/auth
Backend: http://localhost:5000
Admin: http://localhost:81/admin
```

---

## 🔐 LOGIN CREDENTIALS

### Admin Account
```
Email: admin@parlor.com
Password: admin123
```

### Create Customer Account
- Go to: http://localhost:81/auth
- Click "Sign Up"
- Fill details and submit
- Automatic login after registration

---

## 🛠️ COMMON COMMANDS

### Test API
```bash
# Get all services
curl http://localhost:5000/services

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@parlor.com","password":"admin123"}'

# Get festival discount
curl http://localhost:5000/festival-discount
```

### Database
```bash
# Connect to MySQL
mysql -u admin -p -h localhost

# View users
SELECT * FROM users;

# View services
SELECT * FROM services;

# View bookings
SELECT * FROM bookings;

# View discount
SELECT * FROM festival_discount;
```

---

## 📁 FILE LOCATIONS

```
Backend Server:        backend_app.py (Port 5000)
Frontend Server:       frontend_app.py (Port 81)
Database Schema:       database_schema.sql
HTML Pages:
  - Login/Register:    auth.html
  - Admin Panel:       admin_dashboard.html
  - Customer Home:     customer_home.html
Configuration:         requirements.txt
```

---

## 🎯 ADMIN TASKS

### Add Service
1. Login as admin
2. Go to http://localhost:81/admin
3. Click "Add New Service"
4. Fill: Category, Name, Price, Discount
5. Click "Save Service"

### Set Festival Discount
1. Login as admin
2. Go to Discount tab
3. Enter discount percentage
4. Add description
5. Click "Save Discount"

### View Bookings
1. Login as admin
2. Go to Bookings tab
3. See all customer appointments

### Manage Users
1. Login as admin
2. Go to Users tab
3. View all registered customers

---

## 👥 CUSTOMER TASKS

### View Services
1. Login
2. Go to home page
3. Browse all services by category
4. See original and discounted prices

### Book Appointment
1. Click "Book Now" on any service
2. Select date and time
3. Add notes (optional)
4. Confirm booking

### View My Bookings
1. Click "My Bookings" in navigation
2. See all your appointments
3. Cancel if needed

### Update Profile
1. Click "Profile" in navigation
2. Update name, email, phone
3. Save changes

---

## 🎨 CUSTOMIZATION QUICK TIPS

### Change Parlor Name
```
File: auth.html, customer_home.html, admin_dashboard.html
Find: "✨ Parlor Perfect"
Replace: "✨ Your Parlor Name"
```

### Change Contact Number
```
Find: "+919876543210"
Replace: "Your phone number"
In all HTML files
```

### Change Instagram Handle
```
Find: "parlor.perfect"
Replace: "your_handle"
In: customer_home.html, auth.html
```

### Change Location
```
Find: "123 Beauty Lane, Hyderabad..."
Replace: "Your full address"
In: customer_home.html, auth.html
```

### Change Theme Colors
```
In CSS :root variables:
--baby-pink: #FFB6D9;     (Change to your color)
--dark-pink: #FF69B4;     (Change to your color)
```

---

## 🚨 TROUBLESHOOTING

### Port 5000 or 81 already in use?
```bash
# Find what's using the port
lsof -i :5000
lsof -i :81

# Kill process
kill -9 <PID>

# Or use different port:
python backend_app.py --port 5001
```

### Database connection failed?
```bash
# Check MySQL is running
mysql -u root -p -e "SELECT 1"

# Check credentials in backend_app.py
# Default: admin / SuperSecretPass123
```

### Services not loading?
```bash
# Check backend is running
curl http://localhost:5000/services

# Check browser DevTools (F12) for errors
```

### Animations not working?
```bash
# Clear browser cache: Ctrl+Shift+Delete
# Check console for JavaScript errors
# Verify GSAP and Anime.js loaded
```

---

## 📊 SERVICE CATEGORIES

1. **Facials** - Gold, Silver, Diamond
2. **Hydra Facial** - Advanced treatments
3. **Nails** - Manicure, Gel, Art, Pedicure
4. **Waxing** - Face, Arms, Legs, Full Body
5. **Threading** - Eyebrows, Upper Lip, Full Face
6. **Bleach** - Standard, Premium, Face
7. **Hair** - Spa, Smoothening, Coloring
8. **Makeup** - Bridal, Party, Everyday

**Add more categories anytime in admin panel!**

---

## 🔄 API ENDPOINTS QUICK REFERENCE

### Authentication
- `POST /auth/register` - Create account
- `POST /auth/login` - Login
- `GET /auth/verify` - Check token

### Services
- `GET /services` - List all
- `POST /services` - Add (admin)
- `PUT /services/<id>` - Edit (admin)
- `DELETE /services/<id>` - Remove (admin)

### Discount
- `GET /festival-discount` - Get active
- `PUT /festival-discount` - Update (admin)

### Bookings
- `GET /bookings` - View bookings
- `POST /bookings` - Create booking
- `DELETE /bookings/<id>` - Cancel

### Users
- `GET /users/<id>` - Get profile
- `PUT /users/<id>` - Update profile

---

## 📱 BROWSER SUPPORT

✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
✅ Mobile Chrome
✅ Mobile Safari

---

## ⚙️ BACKEND CONFIGURATION

### Change Database Credentials
File: `backend_app.py`
```python
db_config = {
    'host': 'localhost',      # Your DB host
    'user': 'admin',          # Your DB user
    'password': 'password',   # Your DB password
    'database': 'dev'         # Your DB name
}
```

### Change JWT Secret Key
File: `backend_app.py`
```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
JWT_EXPIRATION = 24  # hours
```

### Change Backend Port
File: `backend_app.py`
```python
app.run(host='0.0.0.0', port=5000, debug=True)
# Change 5000 to your port
```

---

## ⚙️ FRONTEND CONFIGURATION

### Change Backend API URL
File: `frontend_app.py`
```python
BACKEND_API = "http://127.0.0.1:5000"
# For AWS: "http://backend-private-ip:5000"
```

### Change Frontend Port
File: `frontend_app.py`
```python
app.run(host='0.0.0.0', port=81, debug=True)
# Change 81 to your port
```

---

## 🚀 DEPLOYMENT CHECKLIST

- [ ] Install Python dependencies
- [ ] Setup MySQL database
- [ ] Update database credentials in backend
- [ ] Test locally
- [ ] Change default admin password
- [ ] Update JWT secret key
- [ ] Configure Nginx
- [ ] Install SSL certificate
- [ ] Update DNS records
- [ ] Setup firewall rules
- [ ] Configure backups
- [ ] Enable monitoring
- [ ] Test all features
- [ ] Go live!

See SETUP_GUIDE.md for detailed deployment steps.

---

## 💡 TIPS & TRICKS

### Bulk Add Services
1. Go to admin dashboard
2. Click "Add New Service"
3. Fill one service
4. Use browser's "Previous" button to fill multiple services faster

### Set Festival Discount
1. Discount applies to ALL services automatically
2. No need to update each service individually
3. Change percentage anytime
4. Customers see discount immediately

### Export Data
1. Use MySQL client
2. Run: `SELECT * FROM services INTO OUTFILE 'services.csv';`
3. Download and share with team

### Monitor Bookings
1. Check admin panel regularly
2. See all bookings by date
3. Track customer preferences
4. Plan staffing accordingly

---

## 📞 SUPPORT LINKS

- **Full Setup Guide**: Read SETUP_GUIDE.md
- **Testing Guide**: Read TESTING_GUIDE.md
- **Project Overview**: Read README.md
- **File Details**: Read FILE_INDEX.md
- **Project Stats**: Read PROJECT_SUMMARY.md

---

## 🎯 PERFORMANCE CHECKLIST

✅ Database indexed properly
✅ Queries optimized
✅ CSS/JS minified
✅ Images optimized
✅ GZIP compression enabled
✅ Cache headers set
✅ CDN ready

---

## 🔐 SECURITY CHECKLIST

✅ JWT tokens used
✅ Passwords hashed
✅ SQL injection prevented
✅ CORS configured
✅ Admin routes protected
✅ Input validated
✅ Error messages safe
✅ Logs secured

---

## ✅ READY TO LAUNCH!

All systems ready. Start with:
```bash
python backend_app.py
python frontend_app.py
```

Then access: **http://localhost:81/auth**

---

**Quick Reference v2.0**
**Parlor Perfect - Beauty Management System**

*Print this card and keep it handy!*

---

### Emergency Commands

```bash
# Restart backend
ps aux | grep backend_app.py
kill <PID>
python backend_app.py

# Restart frontend
ps aux | grep frontend_app.py
kill <PID>
python frontend_app.py

# Check logs
tail -f /var/log/syslog | grep parlor

# Reset database
mysql -u root -p < database_schema.sql

# Test connectivity
curl http://localhost:5000/
```

---

**Made with ❤️ for Beauty Professionals**
