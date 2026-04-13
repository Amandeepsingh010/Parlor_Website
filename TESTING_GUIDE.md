# Parlor Perfect - API Testing Guide & Documentation

---

## Quick Start Testing

### 1. Testing with cURL

#### Register a New User
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+919876543210",
    "password": "password123"
  }'
```

**Expected Response:**
```json
{
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 2,
  "is_admin": 0
}
```

#### Login User
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

#### Get Services (Public)
```bash
curl -X GET http://localhost:5000/services
```

#### Add Service (Admin Only)
```bash
curl -X POST http://localhost:5000/services \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "category": "Facials",
    "service_name": "Platinum Facial",
    "description": "Ultra-premium platinum facial",
    "base_price": 2500,
    "discount_percent": 10
  }'
```

#### Get Festival Discount
```bash
curl -X GET http://localhost:5000/festival-discount
```

#### Update Festival Discount (Admin Only)
```bash
curl -X PUT http://localhost:5000/festival-discount \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "discount_percent": 20,
    "description": "New Year Mega Sale - 20% OFF",
    "is_active": 1
  }'
```

#### Create Booking
```bash
curl -X POST http://localhost:5000/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "user_id": 2,
    "service_id": 1,
    "booking_date": "2024-04-20 14:00:00",
    "notes": "Please prepare for facial"
  }'
```

---

## Web UI Testing Checklist

### Authentication Flow
- [ ] Open http://localhost:81/auth
- [ ] Test Sign Up form
  - [ ] Valid registration
  - [ ] Duplicate email handling
  - [ ] Password validation
  - [ ] Loading animations (makeup brush, scissors, mirror, cucumber)
- [ ] Test Login form
  - [ ] Valid credentials
  - [ ] Invalid credentials
  - [ ] Remember token

### Customer Dashboard (http://localhost:81/)
- [ ] View services grouped by category
- [ ] See festival discount banner (if active)
- [ ] View original and discounted prices
- [ ] Click "Book Now" button
- [ ] Check responsive design on mobile
- [ ] Smooth GSAP animations on scroll

### Services Showcase
- [ ] All 20+ services display correctly
- [ ] Categories filter properly
- [ ] Prices calculate with discounts
- [ ] Service icons display
- [ ] Hover animations work

### Festival Discount Banner
- [ ] Shows when active
- [ ] Displays discount percentage
- [ ] Shows description
- [ ] Applies to service pricing

### Admin Dashboard (http://localhost:81/admin)
- [ ] Navigation menu works
- [ ] Can add new service
- [ ] Can edit service price
- [ ] Can set discount percentage
- [ ] Can delete service
- [ ] Can manage festival discount
- [ ] Can view bookings
- [ ] Can view users

### Services Management
- [ ] Add new service
  - [ ] Select category
  - [ ] Enter service name
  - [ ] Set price
  - [ ] Add discount
  - [ ] Real-time price calculation
- [ ] Edit existing service
- [ ] Delete service
- [ ] See all services in grid

### Discount Management
- [ ] Update discount percentage
- [ ] Change description
- [ ] Enable/disable discount
- [ ] Save changes
- [ ] See preview

### Location & Contact
- [ ] Location displayed correctly
- [ ] Phone link works
- [ ] WhatsApp link works
- [ ] Instagram link works

---

## Database Testing

### Test User Creation
```sql
SELECT * FROM users WHERE email = 'test@example.com';
```

### Test Service Creation
```sql
SELECT * FROM services WHERE category = 'Facials';
```

### Test Booking Creation
```sql
SELECT b.*, u.name, s.service_name 
FROM bookings b 
JOIN users u ON b.user_id = u.id 
JOIN services s ON b.service_id = s.id;
```

### Test Festival Discount
```sql
SELECT * FROM festival_discount WHERE is_active = 1;
```

### Check Password Hashing
```sql
SELECT email, password FROM users;
-- Should see SHA256 hashes, not plaintext
```

---

## Performance Testing

### Load Testing with Apache Bench
```bash
# Test homepage
ab -n 100 -c 10 http://localhost:81/

# Test API endpoint
ab -n 100 -c 10 http://localhost:5000/services
```

### Response Time Check
```bash
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:81/
```

### Database Query Performance
```sql
-- Check slow queries
SELECT * FROM mysql.slow_log;

-- Check query execution time
EXPLAIN SELECT * FROM services WHERE category = 'Facials';
```

---

## Security Testing

### JWT Token Validation
```bash
# Test with invalid token
curl -X GET http://localhost:5000/services/1 \
  -H "Authorization: Bearer invalid_token_here"

# Should return 401 Unauthorized
```

### Admin Protection
```bash
# Try accessing admin endpoint with user token
curl -X POST http://localhost:5000/services \
  -H "Authorization: Bearer USER_TOKEN" \
  -d '{...}'

# Should return 403 Forbidden
```

### SQL Injection Test
```bash
# Try SQL injection
curl "http://localhost:5000/services/1' OR '1'='1"

# Should be safely handled by parameterized queries
```

### CORS Testing
```bash
curl -X OPTIONS http://localhost:5000/ \
  -H "Origin: http://localhost:81" \
  -H "Access-Control-Request-Method: POST"

# Should return CORS headers
```

---

## Animation Testing

### Page Load Animations
- [ ] Watch loading sequence on page load
  - [ ] Makeup brush animation (2s)
  - [ ] Scissors animation (2s)
  - [ ] Mirror animation (2s)
  - [ ] Cucumber spa animation (2.5s)
- [ ] Smooth fade-in of main content

### Scroll Animations
- [ ] Service cards fade in on scroll
- [ ] Feature boxes have hover effects
- [ ] Smooth parallax on hero section
- [ ] Staggered animations on page load

### Interactive Animations
- [ ] Buttons scale on hover (GSAP)
- [ ] Tab switches with animation
- [ ] Modal opens with animation
- [ ] Form inputs focus with glow effect

### Responsive Animations
- [ ] Animations work on mobile
- [ ] No animation lag on slow devices
- [ ] Touch events trigger animations

---

## Browser Compatibility Testing

### Desktop Browsers
- [ ] Chrome 90+
- [ ] Firefox 88+
- [ ] Safari 14+
- [ ] Edge 90+

### Mobile Browsers
- [ ] Chrome Mobile
- [ ] Safari Mobile
- [ ] Firefox Mobile
- [ ] Samsung Browser

### Responsive Breakpoints
- [ ] Desktop (1920px)
- [ ] Laptop (1280px)
- [ ] Tablet (768px)
- [ ] Mobile (375px)

---

## Test Scenarios

### Scenario 1: New User Registration → Booking
1. Open /auth
2. Fill signup form
3. Watch loading animation
4. Redirect to home
5. View services
6. See discount banner
7. Click Book Now
8. Verify booking saved

### Scenario 2: Admin Adding Service
1. Login as admin
2. Go to /admin
3. Click "Add New Service"
4. Fill in all fields
5. Set discount
6. See price calculation
7. Save service
8. Verify in services list

### Scenario 3: Festival Discount Setup
1. Login as admin
2. Go to Discount section
3. Set discount percentage (e.g., 25%)
4. Add description
5. Enable discount
6. Save
7. Logout
8. Login as customer
9. Verify banner shows
10. Verify prices updated

### Scenario 4: Service Price Calculation
1. View service with:
   - Base price: ₹1000
   - Discount: 20%
   - Festival discount: 10%
2. Verify:
   - Original price: ₹1000
   - Service discount: ₹200 (20%)
   - After service discount: ₹800
   - Festival discount calculation

---

## Common Issues & Solutions

### Issue: Animations Not Playing
**Solution:**
```bash
# Check browser console for JavaScript errors
# Ensure GSAP and Anime.js are loaded
# Clear browser cache: Ctrl+Shift+Delete
```

### Issue: Services Not Loading
**Solution:**
```bash
# Check backend is running: curl http://localhost:5000/services
# Check network tab in DevTools
# Verify database connection
```

### Issue: JWT Token Expired
**Solution:**
```bash
# Clear cookies and login again
# Extend token expiration in backend_app.py: JWT_EXPIRATION = 48
```

### Issue: Images Not Loading
**Solution:**
```bash
# Check static file paths
# Verify Nginx configuration for static files
# Clear browser cache
```

---

## Test Data

### Sample Admin Login
```
Email: admin@parlor.com
Password: admin123
```

### Sample Services Added
```
Facials:
- Gold Facial: ₹1500
- Silver Facial: ₹1200
- Diamond Facial: ₹2000

Nails:
- Basic Manicure: ₹300
- Gel Manicure: ₹700

Waxing:
- Face: ₹250
- Arms: ₹350
- Legs: ₹500
- Full Body: ₹1500

... and more
```

### Sample Festival Discount
```
Discount: 15%
Description: "Diwali Special - 15% OFF on all services"
Active: Yes
```

---

## Automated Testing Script

### JavaScript Test Suite (for frontend)
```javascript
// Run in browser console
const tests = {
    testLogin: async () => {
        const response = await fetch('/auth', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                action: 'login',
                email: 'admin@parlor.com',
                password: 'admin123'
            })
        });
        return response.ok;
    },

    testServicesFetch: async () => {
        const response = await fetch('/api/services');
        return response.ok && (await response.json()).length > 0;
    },

    testDiscountFetch: async () => {
        const response = await fetch('/api/festival-discount');
        return response.ok;
    }
};

// Run all tests
Object.entries(tests).forEach(([name, fn]) => {
    fn().then(result => console.log(`${name}: ${result ? '✓' : '✗'}`));
});
```

---

## Performance Benchmarks

### Expected Response Times
```
Frontend homepage load: < 2 seconds
API /services endpoint: < 100ms
Database query average: < 50ms
Full page load with images: < 3 seconds
```

### Expected Metrics
```
Lighthouse Performance: > 80
Lighthouse Accessibility: > 90
Lighthouse Best Practices: > 85
Core Web Vitals: All Green
```

---

## Reporting Issues

When testing, document:
1. **Steps to reproduce**
2. **Expected behavior**
3. **Actual behavior**
4. **Browser & OS**
5. **Screenshots/videos**
6. **Console errors** (F12 → Console tab)

---

## Sign-Off Testing Checklist

- [ ] All pages load without errors
- [ ] Authentication working (login/signup)
- [ ] JWT tokens valid
- [ ] Services CRUD operations work
- [ ] Festival discount works
- [ ] Bookings can be created
- [ ] Admin dashboard functional
- [ ] All animations smooth
- [ ] Mobile responsive
- [ ] Database operations correct
- [ ] No SQL injection vulnerabilities
- [ ] CORS properly configured
- [ ] SSL/TLS working
- [ ] Logs proper
- [ ] Performance acceptable

---

## Deployment Checklist

- [ ] Change all default credentials
- [ ] Update JWT secret key
- [ ] Configure database for production
- [ ] Enable SSL/TLS certificates
- [ ] Setup firewall rules
- [ ] Configure Nginx for production
- [ ] Setup automated backups
- [ ] Configure monitoring alerts
- [ ] Document deployment procedure
- [ ] Create disaster recovery plan
- [ ] Test failover procedures
- [ ] Final security audit

---

## Support Documentation

For users:
- [ ] User guide created
- [ ] Admin guide created
- [ ] FAQ prepared
- [ ] Video tutorials recorded
- [ ] Contact support info visible
- [ ] Help section available

---

**Last Updated**: April 2024
**Version**: 2.0
**Status**: Production Ready
