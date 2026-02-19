# AgriMarket Testing Guide

Complete testing guidelines for the AgriMarket application.

## Quick Start Test

### 1. Register Test Users

Open http://localhost:5000/register and create:

**User 1 - Farmer**
- Name: John Farmer
- Email: farmer@test.com
- Password: test123
- Role: Farmer

**User 2 - Company**
- Name: Agro Industries
- Email: company@test.com
- Password: test123
- Role: Company/Industry

**User 3 - Wholesaler**
- Name: Green Wholesale
- Email: wholesaler@test.com
- Password: test123
- Role: Wholesaler

### 2. Test Farmer Features

**Login as Farmer** (farmer@test.com / test123)

#### Test Crop Products
1. Click "Sell Farm Products" → "Sell Products"
2. Add Product:
   - Name: Tomatoes
   - Description: Fresh organic tomatoes
   - Category: vegetables
   - Price: 5.50
   - Quantity: 100
3. Click "List Product" ✓
4. Verify product appears in list

#### Test Seeds & Fertilizers
1. Click "Sell Products" → "Seeds & Fertilizers"
2. Add Product:
   - Name: NPK Fertilizer
   - Description: Nitrogen-Phosphorus-Potassium mix
   - Category: fertilizer
   - Price: 15.00
   - Quantity: 50
3. Verify product added ✓

#### Test Crop Prediction
1. Click "Crop Prediction"
2. Enter test data:
   - Temperature: 25
   - Humidity: 65
   - Rainfall: 150
   - pH: 6.5
   - Nitrogen: 50
   - Phosphorus: 30
   - Potassium: 200
3. Click "Predict Yield"
4. Should show prediction result ✓

#### Test Disease Detection
1. Click "Disease Detection"
2. Select Crop: Rice
3. Enter symptoms: "Diamond-shaped lesions"
4. Click "Check Disease"
5. Should show disease info ✓

#### Test Insurance
1. Click "Insurance Plans"
2. Create Policy:
   - Crop Type: Rice
   - Coverage Amount: 5000
3. Click "Create Policy"
4. Premium should be $250 (5% of $5000) ✓
5. Policy appears in list ✓

#### Test Orders
1. Click "View Orders"
2. Should show orders from companies buying your products
3. (Will appear after companies place orders)

---

### 3. Test Company Features

**Login as Company** (company@test.com / test123)

#### Test Buy Raw Materials
1. Click "Buy Raw Materials"
2. Should see farmer's products (Tomatoes, etc.)
3. Click "Order Now" for Tomatoes
4. Enter quantity: 10
5. Click "Order Now"
6. Flash message: "Order placed successfully" ✓
7. Verify order quantity decreases ✓

#### Test Sell to Wholesalers
1. Click "Sell to Wholesalers"
2. Process purchased tomatoes and list:
   - Name: Processed Tomato Sauce
   - Description: Premium tomato sauce
   - Price: 8.50
   - Quantity: 30
3. Click "List Product"
4. Product appears ✓

#### Test View Orders
1. Click "View Orders"
2. Should see order from farmer (Tomatoes)
3. Order status: pending ✓

---

### 4. Test Wholesaler Features

**Login as Wholesaler** (wholesaler@test.com / test123)

#### Test Buy Processed Goods
1. Click "Buy Processed Goods"
2. Should see company's products (Tomato Sauce)
3. Enter quantity: 20
4. Click "Order Now"
5. Should show success message ✓

#### Test View Orders
1. Click "View Orders"
2. Shows order for Tomato Sauce (20 units) ✓
3. Status: pending

---

## Functional Testing Checklist

### Authentication
- [ ] Registration with all required fields
- [ ] Registration with duplicate email (should fail)
- [ ] Login with correct credentials
- [ ] Login with wrong credentials (should fail)
- [ ] Logout functionality
- [ ] Session persistence
- [ ] Redirect to login when not authenticated

### Farmer Features
- [ ] Add farm products
- [ ] View own products
- [ ] Edit product details
- [ ] Delete products
- [ ] Crop yield prediction
- [ ] Disease detection for different crops
- [ ] Create insurance policy
- [ ] View insurance policies
- [ ] Add seeds/fertilizers
- [ ] View sales orders

### Company Features
- [ ] View farmer marketplace
- [ ] Search products
- [ ] Purchase products
- [ ] Verify product quantity decreases
- [ ] Add products for wholesalers
- [ ] View own products
- [ ] View purchase orders
- [ ] Order status tracking

### Wholesaler Features
- [ ] View company marketplace
- [ ] Browse processed goods
- [ ] Bulk order (minimum 10 units)
- [ ] Purchase validation
- [ ] View orders
- [ ] Order tracking

### Database
- [ ] Products saved correctly
- [ ] Orders created with correct data
- [ ] User data stored securely
- [ ] Insurance policies saved
- [ ] Predictions logged

### UI/UX
- [ ] Responsive design on mobile
- [ ] Responsive design on tablet
- [ ] Flash messages appear
- [ ] Flash messages auto-close
- [ ] Forms validate correctly
- [ ] Buttons are clickable
- [ ] Links work properly
- [ ] Navigation bar functional

---

## Performance Testing

### Load Testing
```bash
pip install locust

# Create locustfile.py
```

```python
from locust import HttpUser, task, between

class AgriMarketUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def browse_marketplace(self):
        self.client.get("/company/marketplace")

    @task
    def view_products(self):
        self.client.get("/farmer/products")

# Run: locust -f locustfile.py
```

### Response Time Benchmarks
- Home page: < 200ms
- Dashboard: < 300ms
- Marketplace: < 500ms
- Product listing: < 400ms
- Order creation: < 600ms

---

## Security Testing

### 1. SQL Injection
```
# Test in login form
email: admin' OR '1'='1
password: anything
# Should fail gracefully (using MongoDB, not SQL)
```

### 2. XSS Prevention
Add script tag in product name:
```
<script>alert('XSS')</script>
```
Should be escaped and not executed ✓

### 3. CSRF Protection
Test form submissions without valid session

### 4. Authentication Bypass
- Try accessing /farmer/products without login → Redirect to /login ✓
- Try accessing /company/marketplace as farmer → Redirect ✓
- Try accessing /wholesaler/orders as company → Redirect ✓

### 5. Password Security
- Passwords should be hashed (implement in production)
- No password in logs
- No password in error messages

---

## API Testing

### Test with curl or Postman

```bash
# Get product details
curl http://localhost:5000/api/products/[PRODUCT_ID]

# Get user info
curl http://localhost:5000/api/user/[USER_ID]

# Test response format (should be JSON)
curl -H "Accept: application/json" http://localhost:5000/api/products/123
```

### API Response Codes
- 200: Success
- 404: Product not found
- 500: Server error

---

## Cross-Browser Testing

Test on:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile Chrome
- [ ] Mobile Safari

### Checklist
- [ ] CSS renders correctly
- [ ] JavaScript functions work
- [ ] Forms submit properly
- [ ] Navigation works
- [ ] Images load correctly

---

## Regression Testing

After each update:
1. Test all farmer features
2. Test all company features
3. Test all wholesaler features
4. Test authentication
5. Test database operations
6. Test UI responsiveness

---

## Test Data Cleanup

Clear test data:
```python
# MongoDB queries
db.users.deleteMany({"email": "test@test.com"})
db.products.deleteMany({})
db.orders.deleteMany({})
db.insurance.deleteMany({})
```

Or reset entire database:
```bash
mongo
use agri_app
db.dropDatabase()
```

---

## Automated Testing Example

Create `test_app.py`:
```python
import unittest
from app import app
from database.db import users, products

class TestAgriMarket(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.app.post('/register', data={
            'name': 'Test User',
            'email': 'test@test.com',
            'password': 'test123',
            'confirm_password': 'test123',
            'role': 'farmer'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.post('/login', data={
            'email': 'test@test.com',
            'password': 'test123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest test_app.py
```

---

## Known Test Cases

### Edge Cases to Test
1. Empty form submission
2. Very large product quantity
3. Negative prices (should fail)
4. Special characters in names
5. Very long descriptions
6. Multiple rapid requests
7. Concurrent orders for same product
8. Network timeout scenarios

### Expected Behavior
- Form validation prevents invalid data
- User-friendly error messages
- Graceful degradation
- Proper error handling

---

## Reporting Issues

When testing, if you find an issue:

1. **Document the bug:**
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Browser/OS
   - Screenshots

2. **Example issue:**
   ```
   Title: Insurance premium not calculating correctly
   
   Steps:
   1. Go to farmer insurance page
   2. Enter coverage: 1000
   3. Premium shows $500 instead of $50
   
   Expected: $50 (5% of 1000)
   Actual: $500
   
   Browser: Chrome 90
   OS: Windows 10
   ```

---

## Test Results Summary

After completing all tests, document:
- [ ] All features working
- [ ] No critical bugs
- [ ] UI responsive
- [ ] Database operations correct
- [ ] Error handling proper
- [ ] Security issues addressed

---

**Testing Checklist Version**: 1.0  
**Last Updated**: February 2026  
**Status**: Ready for Testing
