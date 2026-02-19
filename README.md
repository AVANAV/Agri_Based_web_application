# AgriMarket - Agricultural Marketplace Platform

A comprehensive web-based agricultural marketplace connecting **Farmers**, **Industries/Companies**, and **Wholesalers** directly without middlemen.

## Features

### For Farmers
- **Crop Yield Prediction**: Machine learning-based crop prediction using environmental factors
- **Disease Detection**: Identify and manage crop diseases with recommended remedies
- **Insurance Plans**: Affordable crop insurance with 5% premium rate
- **Sell Seeds & Fertilizers**: List and sell quality seeds and fertilizers to industries
- **Sell Farm Products**: Directly sell vegetables, fruits, grains, etc., to companies
- **Order Management**: Track all sales orders in real-time

### For Companies/Industries
- **Buy Raw Materials**: Purchase directly from farmers without middlemen
- **Sell to Wholesalers**: List processed goods for wholesaler purchase
- **Order Management**: Track purchases and shipments
- **Direct Farmer Connection**: Access to quality agricultural products

### For Wholesalers
- **Buy Processed Goods**: Purchase finished products from companies
- **Bulk Ordering**: Minimum order requirements with bulk discounts
- **Order Tracking**: Real-time order status updates
- **Direct Company Connection**: Bypass unnecessary intermediaries

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **Machine Learning**: scikit-learn (for crop predictions)
- **Data Processing**: Pandas, NumPy

## Installation Guide

### Prerequisites
- Python 3.7+
- MongoDB (local or cloud instance)
- pip (Python package manager)

### Step 1: Clone or Extract Project
```bash
cd d:\hifebfejf
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv myenv
myenv\Scripts\activate  # On Windows
source myenv/bin/activate  # On Linux/Mac
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure MongoDB
Ensure MongoDB is running:
```bash
# If using local MongoDB
mongod
```

Or update the connection string in `database/db.py` if using MongoDB Atlas (cloud):
```python
client = MongoClient("mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority")
```

### Step 5: Run the Application
```bash
python app.py
```

Access the application at: **http://localhost:5000**

## Project Structure

```
d:\hifebfejf\
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── database/
│   └── db.py                       # MongoDB database setup and functions
├── models/
│   └── crop_model.pkl             # Pre-trained ML model (create this)
├── static/
│   ├── style.css                  # Application styling
│   └── script.js                  # Frontend JavaScript
└── templetes/
    ├── base.html                  # Base template
    ├── index.html                 # Home page
    ├── login.html                 # Login page
    ├── register.html              # Registration page
    ├── farmer_dashboard.html      # Farmer dashboard
    ├── farmer_products.html       # Farmer product listing
    ├── farmer_predict_crop.html   # Crop yield prediction
    ├── farmer_disease_detection.html # Disease detection
    ├── farmer_insurance.html      # Insurance plans
    ├── farmer_seeds_fertilizers.html # Seed & fertilizer selling
    ├── farmer_orders.html         # Farmer order management
    ├── company_dashboard.html     # Company dashboard
    ├── company_marketplace.html   # Company marketplace
    ├── company_sell_wholesaler.html # Sell to wholesalers
    ├── company_orders.html        # Company orders
    ├── wholesaler_dashboard.html  # Wholesaler dashboard
    ├── wholesaler_marketplace.html # Wholesaler marketplace
    ├── wholesaler_orders.html     # Wholesaler orders
    ├── 404.html                   # 404 error page
    └── 500.html                   # 500 error page
```

## API Endpoints

### Authentication
- `GET /` - Home page
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET /dashboard` - Role-based dashboard

### Farmer Routes
- `GET/POST /farmer/products` - List and sell farm products
- `GET/POST /farmer/predict_crop` - Crop yield prediction
- `GET/POST /farmer/disease_detection` - Disease detection
- `GET/POST /farmer/insurance` - Insurance plans
- `GET/POST /farmer/seeds_fertilizers` - Sell seeds & fertilizers
- `GET /farmer/orders` - View sales orders

### Company Routes
- `GET /company/marketplace` - Browse raw materials
- `POST /company/purchase` - Purchase products
- `GET/POST /company/sell_to_wholesaler` - List products for wholesalers
- `GET /company/orders` - View purchase orders

### Wholesaler Routes
- `GET /wholesaler/marketplace` - Browse processed goods
- `POST /wholesaler/purchase` - Purchase products
- `GET /wholesaler/orders` - View orders

### API Routes
- `GET /api/products/<product_id>` - Get product details (JSON)
- `GET /api/user/<user_id>` - Get user info (JSON)

## Database Collections

### users
```json
{
  "_id": ObjectId,
  "name": String,
  "email": String,
  "password": String,
  "role": "farmer|company|wholesaler",
  "created_at": DateTime,
  "is_active": Boolean
}
```

### products
```json
{
  "_id": ObjectId,
  "name": String,
  "description": String,
  "category": String,
  "price": Float,
  "quantity": Integer,
  "farmer_id": ObjectId,
  "image_url": String,
  "created_at": DateTime,
  "is_available": Boolean
}
```

### orders
```json
{
  "_id": ObjectId,
  "buyer_id": ObjectId,
  "seller_id": ObjectId,
  "product_id": ObjectId,
  "quantity": Integer,
  "total_price": Float,
  "status": "pending|confirmed|shipped|delivered",
  "created_at": DateTime
}
```

### insurance
```json
{
  "_id": ObjectId,
  "farmer_id": ObjectId,
  "crop_type": String,
  "coverage_amount": Float,
  "premium": Float,
  "status": "active|expired|claimed",
  "created_at": DateTime,
  "claims": Array
}
```

### crop_predictions
```json
{
  "_id": ObjectId,
  "farmer_id": ObjectId,
  "features": Array,
  "prediction": String,
  "model_type": String,
  "created_at": DateTime
}
```

## Testing the Application

### Sample Accounts
Create accounts with different roles:
1. **Farmer Account**
   - Role: Farmer
   - Access crop prediction, disease detection, insurance, and product listing

2. **Company Account**
   - Role: Company
   - Browse farmer products and list processed goods

3. **Wholesaler Account**
   - Role: Wholesaler
   - Purchase processed goods from companies

### Sample Data Entry
1. Farmers add products (vegetables, seeds, fertilizers)
2. Companies browse and purchase from farmers
3. Wholesalers browse and purchase from companies

## Machine Learning Model Setup

To enable crop prediction:

1. **Create a crop prediction model** (optional):
```python
# Create models/crop_model.pkl
import pickle
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Sample training (replace with actual data)
X = np.array([[25, 60, 150, 6.5, 50, 30, 200], ...])
y = np.array([5000, 4500, 5500, ...])

model = RandomForestRegressor()
model.fit(X, y)

with open('models/crop_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

The model should accept 7 features:
- Temperature (°C)
- Humidity (%)
- Rainfall (mm)
- Soil pH
- Nitrogen (kg/ha)
- Phosphorus (kg/ha)
- Potassium (kg/ha)

## Security Recommendations

### Important for Production:
1. **Hash Passwords**: Use `werkzeug.security` or bcrypt
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

2. **Environment Variables**: Store sensitive data
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   MONGO_URI = os.getenv('MONGO_URI')
   SECRET_KEY = os.getenv('SECRET_KEY')
   ```

3. **HTTPS**: Enable SSL/TLS certificates
4. **CSRF Protection**: Use Flask-WTF
5. **Rate Limiting**: Implement to prevent abuse
6. **Input Validation**: Sanitize all user inputs

## Future Enhancements

- [ ] Payment Gateway Integration (Stripe, PayPal)
- [ ] Email Notifications
- [ ] Real-time Chat System
- [ ] Advanced Analytics Dashboard
- [ ] Mobile App (React Native)
- [ ] API Documentation (Swagger)
- [ ] Unit Tests & Integration Tests
- [ ] Docker Containerization
- [ ] Cloud Deployment (AWS, Heroku)
- [ ] Advanced ML Models
- [ ] Blockchain for Supply Chain Tracking
- [ ] Multi-language Support
- [ ] SMS Notifications

## Troubleshooting

### MongoDB Connection Error
```bash
# Start MongoDB service
# Windows: Go to Services and start MongoDB
# Linux: sudo systemctl start mongod
# Mac: brew services start mongodb-community
```

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host="localhost", port=5001)
```

### Template Not Found
- Ensure `templetes/` folder name is correct (note the typo from original)
- Or rename to `templates/` and update Flask configuration:
```python
app = Flask(__name__, template_folder='templates')
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - Feel free to use this project for educational and commercial purposes.

## Support

For issues, questions, or suggestions, please create an issue or contact the development team.

---

**Built with ❤️ for Agricultural Empowerment**

Happy Farming! 🌾
