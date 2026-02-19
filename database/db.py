from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["agri_app"]

# Collections
users = db["users"]
products = db["products"]
orders = db["orders"]
insurance = db["insurance"]
crop_predictions = db["crop_predictions"]
disease_predictions = db["disease_predictions"]

# Create indexes for better performance
users.create_index("email", unique=True)
products.create_index("farmer_id")
orders.create_index("buyer_id")
orders.create_index("seller_id")
insurance.create_index("farmer_id")
crop_predictions.create_index("farmer_id")
disease_predictions.create_index("farmer_id")

# Database helper functions
def create_user(name, email, password, role):
    """Create a new user"""
    user = {
        "name": name,
        "email": email,
        "password": password,  # Note: In production, hash the password
        "role": role,  # farmer, company, wholesaler, admin
        "created_at": datetime.now(),
        "is_active": True
    }
    return users.insert_one(user)

def find_user_by_email(email):
    """Find user by email"""
    return users.find_one({"email": email})

def find_user_by_id(user_id):
    """Find user by ID"""
    return users.find_one({"_id": ObjectId(user_id)})

def add_product(name, description, category, price, quantity, farmer_id, image_url=""):
    """Add a new product (seeds, fertilizers, raw materials)"""
    product = {
        "name": name,
        "description": description,
        "category": category,  # seeds, fertilizer, vegetables, fruits, grains, etc.
        "price": float(price),
        "quantity": int(quantity),
        "farmer_id": ObjectId(farmer_id),
        "image_url": image_url,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_available": True
    }
    return products.insert_one(product)

def get_products(filter_dict=None, skip=0, limit=10):
    """Get products with optional filters"""
    if filter_dict is None:
        filter_dict = {"is_available": True}
    return list(products.find(filter_dict).skip(skip).limit(limit))

def create_order(buyer_id, seller_id, product_id, quantity, total_price):
    """Create a new order"""
    order = {
        "buyer_id": ObjectId(buyer_id),
        "seller_id": ObjectId(seller_id),
        "product_id": ObjectId(product_id),
        "quantity": int(quantity),
        "total_price": float(total_price),
        "status": "pending",  # pending, confirmed, shipped, delivered, cancelled
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    return orders.insert_one(order)

def create_insurance_policy(farmer_id, crop_type, coverage_amount, premium):
    """Create an insurance policy for a farmer"""
    policy = {
        "farmer_id": ObjectId(farmer_id),
        "crop_type": crop_type,
        "coverage_amount": float(coverage_amount),
        "premium": float(premium),
        "status": "active",  # active, expired, claimed
        "created_at": datetime.now(),
        "expiry_date": None,  # To be set by calculation
        "claims": []
    }
    return insurance.insert_one(policy)

def save_crop_prediction(farmer_id, features, prediction, model_type):
    """Save crop prediction results"""
    prediction_record = {
        "farmer_id": ObjectId(farmer_id),
        "features": features,
        "prediction": prediction,
        "model_type": model_type,  # yield, disease, best_crop, etc.
        "created_at": datetime.now()
    }
    return crop_predictions.insert_one(prediction_record)

def save_disease_prediction(farmer_id, crop_type, image_url, prediction):
    """Save disease prediction results"""
    prediction_record = {
        "farmer_id": ObjectId(farmer_id),
        "crop_type": crop_type,
        "image_url": image_url,
        "disease": prediction,
        "severity": "unknown",  # mild, moderate, severe
        "remedy": "",
        "created_at": datetime.now()
    }
    return disease_predictions.insert_one(prediction_record)
