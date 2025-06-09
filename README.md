# E-commerce Sales Chatbot

A modern e-commerce platform with an intelligent chatbot interface for enhanced customer experience. The platform features a responsive design, secure authentication, and an interactive AI-powered chatbot to assist users with their shopping needs.

## Features

- 🔐 Secure user authentication
- 💬 Interactive chatbot interface with toggle functionality
- 🛍️ Product browsing and search
- 📱 Responsive design for all devices
- 🔍 Advanced product filtering
- 📊 Session management and chat history
- 🎨 Modern Material-UI design

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

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- MongoDB (local installation or MongoDB Atlas account)
- npm or yarn package manager

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

3. Set up environment variables:
Create a `.env` file in the backend directory with the following variables:
```
MONGODB_URI=your_mongodb_connection_string
JWT_SECRET_KEY=your_jwt_secret_key
```

4. Run the backend server:
```bash
python app.py
```
The server will start on http://localhost:5000

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
The application will start on http://localhost:3000

## Login Credentials

You can use the following credentials to log in to the application:

- Email: admin@gmail.com
- Password: admin123

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

## Project Structure

```
├── frontend/               # React frontend application
│   ├── public/            # Static files
│   ├── src/              # Source files
│   │   ├── components/   # React components
│   │   ├── store/       # Redux store
│   │   └── App.tsx      # Main application component
│   └── package.json     # Frontend dependencies
│
├── backend/              # Flask backend server
│   ├── app.py           # Main application file
│   ├── requirements.txt # Python dependencies
│   └── .env            # Environment variables
│
└── README.md           # Project documentation
```

## Features in Detail

### Chatbot Interface
- Toggle button in the bottom-right corner
- Slide-up animation when opening
- Real-time message updates
- Message history
- Loading indicators
- Error handling

### Product Management
- Product listing with images
- Search functionality
- Category filtering
- Price display
- Stock status indicators

### User Authentication
- Secure login/register
- JWT token-based authentication
- Protected routes
- User profile management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team. 