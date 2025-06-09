from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import jwt
import datetime
import bcrypt
from functools import wraps
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client['ecommerce_db']
users_collection = db['users']
products_collection = db['products']
chat_history_collection = db['chat_history']

# JWT configuration
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = users_collection.find_one({'_id': ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({'message': 'Invalid token!'}), 401
        except:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if users_collection.find_one({'email': data['email']}):
        return jsonify({'message': 'Email already exists'}), 400
    
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    user = {
        'email': data['email'],
        'password': hashed_password,
        'name': data['name'],
        'created_at': datetime.datetime.utcnow()
    }
    
    users_collection.insert_one(user)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({'email': data['email']})
    
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user': {
            'id': str(user['_id']),
            'email': user['email'],
            'name': user['name']
        }
    })

# Product routes
@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(products_collection.find())
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

@app.route('/api/products/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    products = list(products_collection.find({
        '$or': [
            {'name': {'$regex': query, '$options': 'i'}},
            {'description': {'$regex': query, '$options': 'i'}}
        ]
    }))
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

# Chatbot routes
@app.route('/api/chat', methods=['POST'])
@token_required
def chat(current_user):
    data = request.get_json()
    message = data.get('message', '')
    
    # Simple chatbot logic - can be enhanced with more sophisticated NLP
    response = process_chat_message(message)
    
    # Store chat history
    chat_history = {
        'user_id': current_user['_id'],
        'message': message,
        'response': response,
        'timestamp': datetime.datetime.utcnow()
    }
    chat_history_collection.insert_one(chat_history)
    
    return jsonify({'response': response})

@app.route('/api/chat/history', methods=['GET'])
@token_required
def get_chat_history(current_user):
    history = list(chat_history_collection.find(
        {'user_id': current_user['_id']}
    ).sort('timestamp', -1).limit(50))
    
    for entry in history:
        entry['_id'] = str(entry['_id'])
        entry['timestamp'] = entry['timestamp'].isoformat()
    
    return jsonify(history)

def process_chat_message(message):
    # Simple response logic - can be enhanced with more sophisticated NLP
    message = message.lower()
    
    if 'hello' in message or 'hi' in message:
        return "Hello! How can I help you today?"
    elif 'product' in message or 'search' in message:
        return "I can help you search for products. What are you looking for?"
    elif 'price' in message:
        return "I can show you our current prices. Which product are you interested in?"
    elif 'help' in message:
        return "I can help you with:\n- Product search\n- Price information\n- Order status\n- General inquiries"
    else:
        return "I'm not sure I understand. Could you please rephrase your question?"

# Initialize database with sample products
def init_db():
    # Clear existing products
    products_collection.delete_many({})
    
    sample_products = [
        # Electronics
        {
            'name': 'Smartphone X',
            'description': 'Latest smartphone with advanced features',
            'price': 999.99,
            'category': 'Electronics',
            'stock': 50,
            'image': 'https://via.placeholder.com/300x200?text=Smartphone+X'
        },
        {
            'name': 'Laptop Pro',
            'description': 'High-performance laptop for professionals',
            'price': 1499.99,
            'category': 'Electronics',
            'stock': 30,
            'image': 'https://via.placeholder.com/300x200?text=Laptop+Pro'
        },
        {
            'name': 'Wireless Earbuds',
            'description': 'Premium wireless earbuds with noise cancellation',
            'price': 199.99,
            'category': 'Electronics',
            'stock': 100,
            'image': 'https://via.placeholder.com/300x200?text=Wireless+Earbuds'
        },
        {
            'name': 'Smart Watch',
            'description': 'Fitness tracker and smartwatch with health monitoring',
            'price': 299.99,
            'category': 'Electronics',
            'stock': 75,
            'image': 'https://via.placeholder.com/300x200?text=Smart+Watch'
        },
        {
            'name': '4K Monitor',
            'description': 'Ultra-wide 4K display for professionals',
            'price': 799.99,
            'category': 'Electronics',
            'stock': 25,
            'image': 'https://via.placeholder.com/300x200?text=4K+Monitor'
        },
        # Clothing
        {
            'name': 'Designer T-Shirt',
            'description': 'Premium cotton t-shirt with modern design',
            'price': 49.99,
            'category': 'Clothing',
            'stock': 200,
            'image': 'https://via.placeholder.com/300x200?text=Designer+T-Shirt'
        },
        {
            'name': 'Denim Jacket',
            'description': 'Classic denim jacket with modern fit',
            'price': 89.99,
            'category': 'Clothing',
            'stock': 60,
            'image': 'https://via.placeholder.com/300x200?text=Denim+Jacket'
        },
        {
            'name': 'Running Shoes',
            'description': 'Lightweight running shoes with advanced cushioning',
            'price': 129.99,
            'category': 'Clothing',
            'stock': 80,
            'image': 'https://via.placeholder.com/300x200?text=Running+Shoes'
        },
        # Home & Kitchen
        {
            'name': 'Smart Coffee Maker',
            'description': 'WiFi-enabled coffee maker with app control',
            'price': 149.99,
            'category': 'Home & Kitchen',
            'stock': 40,
            'image': 'https://via.placeholder.com/300x200?text=Smart+Coffee+Maker'
        },
        {
            'name': 'Air Purifier',
            'description': 'HEPA air purifier for large rooms',
            'price': 199.99,
            'category': 'Home & Kitchen',
            'stock': 35,
            'image': 'https://via.placeholder.com/300x200?text=Air+Purifier'
        },
        # Books
        {
            'name': 'Best Seller Novel',
            'description': 'Award-winning fiction novel',
            'price': 19.99,
            'category': 'Books',
            'stock': 150,
            'image': 'https://via.placeholder.com/300x200?text=Best+Seller+Novel'
        },
        {
            'name': 'Cookbook Collection',
            'description': 'Complete set of gourmet recipes',
            'price': 49.99,
            'category': 'Books',
            'stock': 45,
            'image': 'https://via.placeholder.com/300x200?text=Cookbook+Collection'
        },
        # Sports
        {
            'name': 'Yoga Mat',
            'description': 'Premium non-slip yoga mat',
            'price': 39.99,
            'category': 'Sports',
            'stock': 120,
            'image': 'https://via.placeholder.com/300x200?text=Yoga+Mat'
        },
        {
            'name': 'Dumbbell Set',
            'description': 'Adjustable weight dumbbell set',
            'price': 149.99,
            'category': 'Sports',
            'stock': 30,
            'image': 'https://via.placeholder.com/300x200?text=Dumbbell+Set'
        },
        # Beauty
        {
            'name': 'Skincare Set',
            'description': 'Complete skincare routine set',
            'price': 79.99,
            'category': 'Beauty',
            'stock': 90,
            'image': 'https://via.placeholder.com/300x200?text=Skincare+Set'
        },
        {
            'name': 'Perfume Collection',
            'description': 'Luxury fragrance collection',
            'price': 199.99,
            'category': 'Beauty',
            'stock': 25,
            'image': 'https://via.placeholder.com/300x200?text=Perfume+Collection'
        },
        # Toys
        {
            'name': 'Educational Robot',
            'description': 'Interactive learning robot for kids',
            'price': 89.99,
            'category': 'Toys',
            'stock': 55,
            'image': 'https://via.placeholder.com/300x200?text=Educational+Robot'
        },
        {
            'name': 'Building Blocks Set',
            'description': 'Creative building blocks for all ages',
            'price': 59.99,
            'category': 'Toys',
            'stock': 70,
            'image': 'https://via.placeholder.com/300x200?text=Building+Blocks+Set'
        },
        # Office
        {
            'name': 'Ergonomic Chair',
            'description': 'Comfortable office chair with lumbar support',
            'price': 299.99,
            'category': 'Office',
            'stock': 20,
            'image': 'https://via.placeholder.com/300x200?text=Ergonomic+Chair'
        },
        {
            'name': 'Wireless Keyboard',
            'description': 'Slim wireless keyboard with numeric pad',
            'price': 69.99,
            'category': 'Office',
            'stock': 85,
            'image': 'https://via.placeholder.com/300x200?text=Wireless+Keyboard'
        },
        # Garden
        {
            'name': 'Smart Garden Kit',
            'description': 'Automated indoor garden system',
            'price': 199.99,
            'category': 'Garden',
            'stock': 40,
            'image': 'https://via.placeholder.com/300x200?text=Smart+Garden+Kit'
        },
        {
            'name': 'Garden Tools Set',
            'description': 'Complete set of gardening tools',
            'price': 79.99,
            'category': 'Garden',
            'stock': 60,
            'image': 'https://via.placeholder.com/300x200?text=Garden+Tools+Set'
        }
    ]
    products_collection.insert_many(sample_products)
    print("Database initialized with", len(sample_products), "products")

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 