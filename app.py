from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from google import genai

# 1. App Setup
app = Flask(__name__)
CORS(app) 

# --- DATABASE CONFIGURATION ---
DATABASE_URL = "postgresql://postgres.ynpnuitpxbskgxzzojpw:G4L2xUnZzBVJxW21@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres"

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2. Database Models
class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)  
    title = db.Column(db.String(100), nullable=False)       
    duration = db.Column(db.String(20), nullable=False)     
    price = db.Column(db.String(20), nullable=False)        
    image = db.Column(db.String(100), nullable=False)       
    category = db.Column(db.String(50), default='General')
    overview = db.Column(db.Text, nullable=True)
    itinerary = db.Column(db.Text, nullable=True)
    inclusions = db.Column(db.String(200), nullable=True)

# 🌟 NEW: WISHLIST DATABASE MODEL 🌟
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    
    # Relationship to easily fetch the actual package details later
    package = db.relationship('Package', backref=db.backref('wishlisted_by', lazy=True))

# Create tables in the database
with app.app_context():
    db.create_all()

# --- AI CHATBOT SETUP (NEW SDK) ---
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 3. API Routes
@app.route('/api/packages/<destination>', methods=['GET'])
def get_packages(destination):
    packages = Package.query.filter_by(destination=destination).all()
    result = []
    for p in packages:
        result.append({
            "id": p.id, "n": p.title, "d": p.duration, 
            "p": p.price, "i": p.image, "over": p.overview, 
            "itin": p.itinerary, "inc": p.inclusions, "cat": p.category
        })
    return jsonify(result)

@app.route('/api/packages/all', methods=['GET'])
def get_all_packages():
    packages = Package.query.all()
    result = []
    for p in packages:
        result.append({
            "id": p.id, "destination": p.destination, "title": p.title, 
            "price": p.price, "duration": p.duration, "image": p.image,
            "category": p.category, "overview": p.overview, 
            "itinerary": p.itinerary, "inclusions": p.inclusions
        })
    return jsonify(result)

@app.route('/api/packages', methods=['POST'])
def add_package():
    data = request.json
    new_package = Package(
        destination=data['destination'], title=data['title'], duration=data['duration'],
        price=data['price'], image=data['image'], category=data.get('category', 'General'),
        overview=data.get('overview', ''), itinerary=data.get('itinerary', ''),
        inclusions=data.get('inclusions', '')
    )
    db.session.add(new_package)
    db.session.commit()
    return jsonify({"message": f"Successfully added {data['title']}!"}), 201

@app.route('/api/packages/<int:package_id>', methods=['PUT'])
def update_package(package_id):
    package = Package.query.get(package_id)
    if package:
        data = request.json
        package.destination = data['destination']
        package.title = data['title']
        package.duration = data['duration']
        package.price = data['price']
        package.image = data['image']
        package.category = data.get('category', 'General')
        package.overview = data.get('overview', '')
        package.itinerary = data.get('itinerary', '')
        package.inclusions = data.get('inclusions', '')
        db.session.commit()
        return jsonify({"message": f"Successfully updated {package.title}!"}), 200
    return jsonify({"message": "Package not found!"}), 404

@app.route('/api/packages/<int:package_id>', methods=['DELETE'])
def delete_package(package_id):
    package = Package.query.get(package_id)
    if package:
        db.session.delete(package)
        db.session.commit()
        return jsonify({"message": "Deleted successfully!"}), 200
    return jsonify({"message": "Not found!"}), 404

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == "admin" and data.get('password') == "Aura2026":
        return jsonify({"success": True, "message": "Login Successful!"}), 200
    return jsonify({"success": False, "message": "Invalid Credentials!"}), 401

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"reply": "Please say something!"}), 400

        packages = Package.query.all()
        
        if packages:
            pkg_list = "\n".join([f"- {p.title} ({p.destination}): {p.duration} for ₹{p.price}" for p in packages])
            db_context = f"Here is our live database of packages:\n{pkg_list}\n\nRule: ONLY recommend packages from this list. Do not make up packages."
        else:
            db_context = "Currently, no packages are available."

        system_prompt = f"You are a friendly AI travel assistant for Aura Holidays. Keep your answers short (2-3 sentences max) and enthusiastic.\n\n{db_context}"
        full_prompt = f"{system_prompt}\n\nUser: {user_message}\nAI:"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        return jsonify({"reply": response.text})
        
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"reply": "Sorry, my AI brain is taking a quick nap! Please try again."}), 500

# 🌟 AI CUSTOM ITINERARY GENERATOR 🌟
@app.route('/api/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
        data = request.json
        dest = data.get('destination')
        days = data.get('days')
        budget = data.get('budget')
        vibe = data.get('vibe')

        system_prompt = f"""
        You are an expert, luxury travel planner for 'Aura Holidays'. 
        The user wants a {days}-day trip to {dest}.
        Their total budget is ₹{budget}.
        The desired travel vibe is: {vibe}.
        
        CRITICAL RULES FOR OUTPUT:
        1. Write the entire response STRICTLY in clean, beautiful HTML format. Do NOT use markdown (no ```html tags).
        2. Use <h4 style="color:#0f766e; font-weight:bold; margin-top:20px; border-bottom:1px solid #eee; padding-bottom:5px;"> for Day headings (e.g., Day 1: Arrival).
        3. Use <ul style="list-style-type:disc; padding-left:20px; margin-bottom:15px; color:#4b5563;"> and <li> for the activities.
        4. Bold the timings (e.g., <b>Morning:</b>).
        5. Add a short, enthusiastic intro paragraph and a brief concluding thought at the end within <p> tags.
        6. Keep it realistic based on the budget!
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=system_prompt
        )
        
        raw_html = response.text.replace('```html', '').replace('```', '').strip()
        return jsonify({"itinerary": raw_html})
        
    except Exception as e:
        print(f"AI Generator Error: {e}")
        return jsonify({"error": "Our AI brain is taking a quick nap. Please try again!"}), 500

# 🌟 NEW: GET USER'S WISHLIST 🌟
@app.route('/api/wishlist/<email>', methods=['GET'])
def get_wishlist(email):
    saved_items = Wishlist.query.filter_by(user_email=email).all()
    saved_package_ids = [item.package_id for item in saved_items]
    return jsonify(saved_package_ids), 200

# 🌟 NEW: TOGGLE (ADD/REMOVE) WISHLIST ITEM 🌟
@app.route('/api/wishlist/toggle', methods=['POST'])
def toggle_wishlist():
    data = request.json
    email = data.get('email')
    package_id = data.get('package_id')
    action = data.get('action')

    if not email or not package_id:
        return jsonify({"error": "Email and Package ID are required"}), 400

    if action == 'add':
        existing = Wishlist.query.filter_by(user_email=email, package_id=package_id).first()
        if not existing:
            new_wishlist_item = Wishlist(user_email=email, package_id=package_id)
            db.session.add(new_wishlist_item)
            db.session.commit()
            return jsonify({"message": "Added to wishlist"}), 201
            
    elif action == 'remove':
        item_to_remove = Wishlist.query.filter_by(user_email=email, package_id=package_id).first()
        if item_to_remove:
            db.session.delete(item_to_remove)
            db.session.commit()
            return jsonify({"message": "Removed from wishlist"}), 200

    return jsonify({"message": "No action taken"}), 200

if __name__ == '__main__':
    app.run(debug=True)