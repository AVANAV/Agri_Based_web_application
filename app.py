from flask import Flask, render_template, request, redirect, session, jsonify, flash
from database.db import (
    users, products, orders, insurance, crop_predictions,
    find_user_by_email, find_user_by_id, create_user, add_product,
    get_products, create_order, create_insurance_policy, save_crop_prediction
)
from bson.objectid import ObjectId
from datetime import datetime
import pickle
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_change_this_in_production"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        if not all([name, email, password, confirm_password, role]):
            flash("All fields are required", "error")
            return redirect("/register")

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect("/register")

       
        if find_user_by_email(email):
            flash("Email already registered", "error")
            return redirect("/register")

      
        try:
            create_user(name, email, password, role)
            flash("Registration successful! Please login.", "success")
            return redirect("/login")
        except Exception as e:
            flash("Registration failed", "error")
            return redirect("/register")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = find_user_by_email(email)
        if user and user["password"] == password:
            session["user_id"] = str(user["_id"])
            session["user_name"] = user["name"]
            session["role"] = user["role"]
            flash(f"Welcome {user['name']}", "success")
            return redirect("/dashboard")
        else:
            flash("Invalid email or password", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "success")
    return redirect("/")

# ==================== DASHBOARD ROUTES ====================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    role = session.get("role")

    if role == "farmer":
        return render_template("farmer_dashboard.html", user=session)
    elif role == "company":
        return render_template("company_dashboard.html", user=session)
    elif role == "wholesaler":
        return render_template("wholesaler_dashboard.html", user=session)
    else:
        return redirect("/")

# ==================== FARMER ROUTES ====================

@app.route("/farmer/products", methods=["GET", "POST"])
def farmer_products():
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        try:
            add_product(name, description, category, price, quantity, session["user_id"])
            flash("Product added successfully", "success")
        except Exception as e:
            flash("Error adding product", "error")

        return redirect("/farmer/products")

    # Get farmer's products
    farmer_products_list = list(products.find({"farmer_id": ObjectId(session["user_id"])}))
    return render_template("farmer_products.html", products=farmer_products_list)

@app.route("/farmer/predict_crop", methods=["GET", "POST"])
def predict_crop():
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")

    prediction = None
    if request.method == "POST":
        try:
            # Load model
            if os.path.exists("models/crop_model.pkl"):
                model = pickle.load(open("models/crop_model.pkl", "rb"))
                features = [float(x) for x in request.form.values()]
                prediction = model.predict([features])[0]
                
                # Save prediction to database
                save_crop_prediction(session["user_id"], features, str(prediction), "crop_yield")
                flash("Prediction saved successfully", "success")
            else:
                flash("Model not found. Please ensure crop_model.pkl exists in models folder", "error")
        except Exception as e:
            flash(f"Prediction error: {str(e)}", "error")

    return render_template("farmer_predict_crop.html", prediction=prediction)

@app.route("/farmer/disease_detection", methods=["GET", "POST"])
def disease_detection():
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")

    if request.method == "POST":
        crop_type = request.form.get("crop_type")
        disease_description = request.form.get("disease_description")
        
        try:
            # Simple disease detection (can be enhanced with ML model)
            diseases = {
                "rice": ["leaf_blast", "brown_spot", "bacterial_leaf_blight"],
                "wheat": ["powdery_mildew", "rust", "septoria_nodorum_blotch"],
                "corn": ["common_rust", "northern_leaf_blight", "gray_leaf_spot"],
                "tomato": ["early_blight", "late_blight", "powdery_mildew"]
            }
            
            detected_disease = "Not detected"
            if crop_type.lower() in diseases:
                detected_disease = "Common diseases: " + ", ".join(diseases[crop_type.lower()])
            
            flash(f"Disease Detection: {detected_disease}", "info")
        except Exception as e:
            flash("Error in disease detection", "error")

    return render_template("farmer_disease_detection.html")

@app.route("/farmer/insurance", methods=["GET", "POST"])
def farmer_insurance():
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")

    if request.method == "POST":
        crop_type = request.form.get("crop_type")
        coverage_amount = request.form.get("coverage_amount")
        
        # Premium calculation: 5% of coverage amount
        premium = float(coverage_amount) * 0.05
        
        try:
            create_insurance_policy(session["user_id"], crop_type, coverage_amount, premium)
            flash(f"Insurance policy created! Premium: ${premium:.2f}", "success")
        except Exception as e:
            flash("Error creating insurance policy", "error")

        return redirect("/farmer/insurance")

    # Get farmer's policies
    farmer_policies = list(insurance.find({"farmer_id": ObjectId(session["user_id"])}))
    return render_template("farmer_insurance.html", policies=farmer_policies)

@app.route("/farmer/seeds_fertilizers", methods=["GET", "POST"])
def seeds_fertilizers():
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")  # seeds, fertilizer
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        try:
            add_product(name, description, category, price, quantity, session["user_id"])
            flash("Product added successfully", "success")
        except Exception as e:
            flash("Error adding product", "error")

        return redirect("/farmer/seeds_fertilizers")

    farmer_products_list = list(products.find({
        "farmer_id": ObjectId(session["user_id"]),
        "category": {"$in": ["seeds", "fertilizer"]}
    }))
    return render_template("farmer_seeds_fertilizers.html", products=farmer_products_list)

@app.route("/farmer/orders", methods=["GET"])
def farmer_orders():
    if "user_id" not in session or session.get("role") != "farmer":
        return redirect("/login")

    farmer_orders_list = list(orders.find({"seller_id": ObjectId(session["user_id"])}))
    return render_template("farmer_orders.html", orders=farmer_orders_list)

# ==================== COMPANY/INDUSTRY ROUTES ====================

@app.route("/company/marketplace", methods=["GET"])
def company_marketplace():
    if "user_id" not in session or session.get("role") != "company":
        return redirect("/login")

    # Get all products from farmers
    all_products = list(products.find({"is_available": True}))
    return render_template("company_marketplace.html", products=all_products)

@app.route("/company/purchase", methods=["POST"])
def company_purchase():
    if "user_id" not in session or session.get("role") != "company":
        return jsonify({"error": "Unauthorized"}), 403

    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")

    try:
        product = products.find_one({"_id": ObjectId(product_id)})
        if not product:
            return jsonify({"error": "Product not found"}), 404

        seller_id = product["farmer_id"]
        total_price = float(product["price"]) * int(quantity)

        order_id = create_order(session["user_id"], str(seller_id), product_id, quantity, total_price)
        
        # Update product quantity
        products.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"quantity": -int(quantity)}}
        )

        flash("Order placed successfully", "success")
        return redirect("/company/orders")
    except Exception as e:
        flash(f"Error placing order: {str(e)}", "error")
        return redirect("/company/marketplace")

@app.route("/company/sell_to_wholesaler", methods=["GET", "POST"])
def company_sell_to_wholesaler():
    if "user_id" not in session or session.get("role") != "company":
        return redirect("/login")

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        try:
            add_product(name, description, "processed_goods", price, quantity, session["user_id"])
            flash("Product listed for wholesalers", "success")
        except Exception as e:
            flash("Error listing product", "error")

        return redirect("/company/sell_to_wholesaler")

    company_products = list(products.find({
        "farmer_id": ObjectId(session["user_id"]),
        "category": "processed_goods"
    }))
    return render_template("company_sell_wholesaler.html", products=company_products)

@app.route("/company/orders", methods=["GET"])
def company_orders():
    if "user_id" not in session or session.get("role") != "company":
        return redirect("/login")

    company_orders_list = list(orders.find({"buyer_id": ObjectId(session["user_id"])}))
    return render_template("company_orders.html", orders=company_orders_list)

# ==================== WHOLESALER ROUTES ====================

@app.route("/wholesaler/marketplace", methods=["GET"])
def wholesaler_marketplace():
    if "user_id" not in session or session.get("role") != "wholesaler":
        return redirect("/login")

    all_products = list(products.find({
        "is_available": True,
        "category": "processed_goods"
    }))
    return render_template("wholesaler_marketplace.html", products=all_products)

@app.route("/wholesaler/purchase", methods=["POST"])
def wholesaler_purchase():
    if "user_id" not in session or session.get("role") != "wholesaler":
        return jsonify({"error": "Unauthorized"}), 403

    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")

    try:
        product = products.find_one({"_id": ObjectId(product_id)})
        if not product:
            return jsonify({"error": "Product not found"}), 404

        seller_id = product["farmer_id"]
        total_price = float(product["price"]) * int(quantity)

        order_id = create_order(session["user_id"], str(seller_id), product_id, quantity, total_price)

        products.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"quantity": -int(quantity)}}
        )

        flash("Order placed successfully", "success")
        return redirect("/wholesaler/orders")
    except Exception as e:
        flash(f"Error placing order: {str(e)}", "error")
        return redirect("/wholesaler/marketplace")

@app.route("/wholesaler/orders", methods=["GET"])
def wholesaler_orders():
    if "user_id" not in session or session.get("role") != "wholesaler":
        return redirect("/login")

    wholesaler_orders_list = list(orders.find({"buyer_id": ObjectId(session["user_id"])}))
    return render_template("wholesaler_orders.html", orders=wholesaler_orders_list)

# ==================== API ROUTES ====================

@app.route("/api/products/<product_id>")
def get_product(product_id):
    try:
        product = products.find_one({"_id": ObjectId(product_id)})
        if product:
            product["_id"] = str(product["_id"])
            product["farmer_id"] = str(product["farmer_id"])
            return jsonify(product)
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/user/<user_id>")
def get_user_info(user_id):
    try:
        user = find_user_by_id(user_id)
        if user:
            user["_id"] = str(user["_id"])
            del user["password"]  # Don't send password
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
