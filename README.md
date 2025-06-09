# E-commerce Sales Chatbot

A modern e-commerce platform with an intelligent chatbot interface for enhanced customer experience.

## Features

- 🔐 Secure user authentication
- 💬 Interactive chatbot interface
- 🛍️ Product browsing and search
- 📱 Responsive design for all devices
- 🔍 Advanced product filtering
- 📊 Session management and chat history

## Tech Stack

### Frontend
- React with TypeScript
- Material-UI for modern components
- Redux for state management
- Axios for API calls

### Backend
- Python Flask
- MongoDB for data storage
- JWT for authentication
- Flask-CORS for cross-origin support

## Project Structure

```
├── frontend/               # React frontend application
├── backend/               # Flask backend server
├── docs/                  # Documentation
└── README.md             # Project documentation
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up MongoDB:
- Install MongoDB locally or use MongoDB Atlas
- Update the connection string in `backend/config.py`

4. Run the backend server:
```bash
python app.py
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Documentation

### Authentication Endpoints
- POST /api/auth/register - Register new user
- POST /api/auth/login - User login
- GET /api/auth/profile - Get user profile

### Product Endpoints
- GET /api/products - Get all products
- GET /api/products/{id} - Get product by ID
- GET /api/products/search - Search products

### Chatbot Endpoints
- POST /api/chat - Send message to chatbot
- GET /api/chat/history - Get chat history

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 