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
    if products_collection.count_documents({}) == 0:
        sample_products = [
            {
                'name': 'Smartphone X',
                'description': 'Latest smartphone with advanced features',
                'price': 999.99,
                'category': 'Electronics',
                'stock': 50
            },
            {
                'name': 'Laptop Pro',
                'description': 'High-performance laptop for professionals',
                'price': 1499.99,
                'category': 'Electronics',
                'stock': 30
            },
            {
                'name': 'Wireless Earbuds',
                'description': 'Premium wireless earbuds with noise cancellation',
                'price': 199.99,
                'category': 'Electronics',
                'stock': 100
            }
        ]
        products_collection.insert_many(sample_products)

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 