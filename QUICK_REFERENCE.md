# AgriMarket - Quick Reference Guide

## Getting Started (5 minutes)

### 1. Installation
```bash
# Navigate to project
cd d:\hifebfejf

# Activate virtual environment
myenv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Start Application
```bash
# Make sure MongoDB is running
mongod

# Run Flask app
python app.py

# Open http://localhost:5000
```

### 3. Create Test Account
- Go to http://localhost:5000/register
- Fill in details (choose your role)
- Log in with created account

---

## Key URLs

| Page | URL | Role |
|------|-----|------|
| Home | `/` | All |
| Register | `/register` | All |
| Login | `/login` | All |
| Dashboard | `/dashboard` | Logged In |
| Logout | `/logout` | Logged In |
| **Farmer Routes** | | |
| Sell Products | `/farmer/products` | Farmer |
| Crop Prediction | `/farmer/predict_crop` | Farmer |
| Disease Detection | `/farmer/disease_detection` | Farmer |
| Insurance | `/farmer/insurance` | Farmer |
| Seeds & Fertilizers | `/farmer/seeds_fertilizers` | Farmer |
| My Orders | `/farmer/orders` | Farmer |
| **Company Routes** | | |
| Buy Raw Materials | `/company/marketplace` | Company |
| Sell to Wholesalers | `/company/sell_to_wholesaler` | Company |
| Orders | `/company/orders` | Company |
| **Wholesaler Routes** | | |
| Buy Products | `/wholesaler/marketplace` | Wholesaler |
| Orders | `/wholesaler/orders` | Wholesaler |
| **API Routes** | | |
| Get Product | `/api/products/<id>` | All |
| Get User | `/api/user/<id>` | All |

---

## Default Test Credentials

After first setup, use these to test:

```
Email: farmer@test.com
Password: test123
Role: Farmer

Email: company@test.com
Password: test123
Role: Company

Email: wholesaler@test.com
Password: test123
Role: Wholesaler
```

---

## Database Commands

### Connect to MongoDB
```bash
mongo  # or mongosh
```

### Useful Queries
```javascript
// View users
db.users.find()

// View products
db.products.find()

// View orders
db.orders.find()

// Count total products
db.products.countDocuments()

// Find farmer products
db.products.find({category: "vegetables"})

// Delete test data
db.users.deleteMany({email: "test@test.com"})
```

---

## Flask Commands

```bash
# Run in debug mode (default)
python app.py

# Run on different port
python -c "from app import app; app.run(port=5001)"

# Generate shell
flask shell

# Run with gunicorn (production)
gunicorn app:app
```

---

## File Editing Quick Guide

### app.py
- Add new routes here
- Modify existing functionality
- Add error handlers

### database/db.py
- Create new functions for database operations
- Add new collections
- Create indexes

### templetes/
- Create new HTML pages
- Modify existing layouts
- Add form fields

### static/style.css
- Update styling
- Add new components
- Modify colors/fonts

### static/script.js
- Add JavaScript functionality
- Implement validation
- Add event handlers

---

## Common Tasks

### Add New Product Category
1. Edit `config.py` - Add to `PRODUCT_CATEGORIES`
2. Edit relevant HTML template
3. Add to database query filters (if needed)

### Add New Feature for Farmers
1. Create route in `app.py`
2. Create database function in `database/db.py`
3. Create HTML template in `templetes/`
4. Add link in `farmer_dashboard.html`
5. Add CSS styling in `static/style.css`

### Add New API Endpoint
```python
@app.route("/api/new_endpoint/<param>")
def new_endpoint(param):
    try:
        # Your logic here
        return jsonify({"result": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
```

### Add New Database Collection
```python
# In database/db.py
new_collection = db["collection_name"]
new_collection.create_index("field_name")

# Create helper function
def add_to_collection(data):
    return new_collection.insert_one(data)
```

---

## Testing Workflow

### Manual Testing
1. Register 3 accounts (Farmer, Company, Wholesaler)
2. Test each role's features
3. Test complete supply chain flow
4. Check database for saved data

### Automated Testing
```bash
python -m unittest test_app.py
```

### Performance Testing
```bash
# Using locust
locust -f locustfile.py
```

---

## Debugging Tips

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.debug("Your message here")
```

### Check Request Data
```python
@app.route("/test", methods=["POST"])
def test():
    print(request.form)  # See form data
    print(request.files)  # See uploaded files
    print(request.json)   # See JSON data
```

### MongoDB Debug
```python
# See all operations
import logging
logging.getLogger('pymongo').setLevel(logging.DEBUG)
```

### Browser Console
- Press F12 in browser
- Check Console tab for JavaScript errors
- Use Network tab to see API calls

---

## Deployment Checklist

Before going to production:
- [ ] Change SECRET_KEY in app.py
- [ ] Set FLASK_ENV=production
- [ ] Enable password hashing
- [ ] Configure MongoDB Atlas
- [ ] Set up HTTPS/SSL
- [ ] Enable CSRF protection
- [ ] Set up logging
- [ ] Create .env file
- [ ] Test all features
- [ ] Load test application

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: Flask` | Missing dependencies | `pip install -r requirements.txt` |
| `ConnectionFailure` | MongoDB not running | Start MongoDB with `mongod` |
| `Address already in use` | Port 5000 occupied | Change port or kill process |
| `Template not found` | Wrong folder path | Check `templetes/` spelling |
| `KeyError` | Missing form field | Verify form POST data |
| `ObjectId is invalid` | Bad MongoDB ID | Verify ID format |

---

## Configuration Quick Ref

### app.py Settings
```python
app.secret_key = "your-secret-here"  # Change this!
app.run(debug=True, host="localhost", port=5000)
```

### Database Connection
```python
# database/db.py
client = MongoClient("mongodb://localhost:27017/")
db = client["agri_app"]
```

### Session Settings
```python
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SESSION_COOKIE_SECURE = False  # True in production
```

---

## Python/Flask Snippets

### Add Flash Message
```python
from flask import flash
flash("Success message", "success")  # Or "error", "info"
```

### Check User Role
```python
if session.get("role") != "farmer":
    return redirect("/login")
```

### Query Database
```python
user = users.find_one({"_id": ObjectId(user_id)})
products_list = list(products.find({"category": "seeds"}))
```

### Create ObjectId
```python
from bson.objectid import ObjectId
oid = ObjectId(id_string)
```

### Render Template with Data
```python
return render_template("page.html", products=products_list, user=user)
```

---

## HTML/CSS Snippets

### Form Group
```html
<div class="form-group">
    <label for="field">Label:</label>
    <input type="text" id="field" name="field" required>
</div>
```

### Button
```html
<button type="submit" class="btn btn-primary">Submit</button>
```

### Alert
```html
<div class="alert alert-success">Success message!</div>
```

### Product Card
```html
<div class="product-card">
    <h4>Product Name</h4>
    <p>Description</p>
    <p class="price">$99.99</p>
</div>
```

---

## JavaScript Snippets

### Validate Form
```javascript
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required]');
    inputs.forEach(input => {
        if (!input.value) {
            input.style.borderColor = 'red';
        }
    });
}
```

### Show Toast
```javascript
showToast("Message here", "success");
```

### Fetch API
```javascript
fetch('/api/products/123')
    .then(r => r.json())
    .then(data => console.log(data));
```

---

## Performance Optimization

### Database
- Use indexes (already done)
- Limit query results: `.limit(10)`
- Select only needed fields

### Frontend
- Minify CSS/JavaScript
- Compress images
- Use CDN for static files

### Backend
- Enable caching for static files
- Use connection pooling
- Optimize queries

---

## Project Structure at Glance

```
app.py               ← Main application (30+ routes)
database/db.py       ← Database functions
config.py            ← Configuration
requirements.txt     ← Dependencies
static/
  ├── style.css     ← Styling (800+ lines)
  └── script.js     ← Frontend logic (400+ lines)
templetes/           ← HTML templates (15 pages)
├── README.md        ← Full documentation
├── TESTING.md       ← Test guide
├── DEPLOYMENT.md    ← Production guide
└── (This file)      ← Quick reference
```

---

## Getting Help

1. **Check Documentation**: README.md has comprehensive info
2. **Test Guide**: TESTING.md has step-by-step tests
3. **Deployment Guide**: DEPLOYMENT.md for production
4. **Code Comments**: Read inline comments in code
5. **Flask Docs**: https://flask.palletsprojects.com/
6. **MongoDB Docs**: https://docs.mongodb.com/

---

## Version Info

- **AgriMarket**: v1.0
- **Python**: 3.7+
- **Flask**: 3.1.2
- **MongoDB**: 4.0+
- **Status**: Production Ready

---

**Last Updated**: February 14, 2026  
**Maintained by**: AgriMarket Development Team

Keep this guide handy for quick reference during development!
