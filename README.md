# Expense Tracker Application

A simple expense tracker application with user authentication, built with FastAPI (backend) and React (frontend).

## Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy
- Pydantic
- MySQL
- JWT Authentication

**Frontend:**
- React.js
- React Router
- Axios
- Basic CSS

## Project Structure

```
expenses tracking/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models (User, Expense)
│   │   ├── schemas/         # Pydantic schemas for validation
│   │   ├── routes/          # API endpoints (auth, expenses, dashboard)
│   │   ├── database/        # Database configuration
│   │   ├── auth/            # Authentication utilities
│   │   ├── utils/           # Utility functions (env config)
│   │   └── main.py          # FastAPI application entry point
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── pages/           # React page components (Login, Register, Dashboard, Expenses)
│   │   ├── services/        # API service (Axios configuration)
│   │   ├── App.jsx          # Main App component with routing
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
├── DATABASE_DESIGN.md       # Database documentation
└── API_DOCUMENTATION.md     # Complete API documentation
```

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed
2. **Node.js 16+** installed
3. **MySQL 8.0+** installed and running

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
- Open `backend/.env`
- Update `DATABASE_URL` with your MySQL credentials:
  ```
  mysql+pymysql://your_username:your_password@localhost/expense_tracker
  ```
- Update `SECRET_KEY` with a secure random string

6. Create MySQL database:
```sql
CREATE DATABASE expense_tracker;
```

Or run the SQL queries from `DATABASE_DESIGN.md`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start Backend Server

```bash
cd backend
venv\Scripts\activate  # Windows
python -m uvicorn app.main:app --reload
```

Backend will run on: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend will run on: `http://localhost:5173`

## Application Features

### Authentication
- User registration with username, email, and password
- User login with JWT token authentication
- Protected routes for authenticated users
- Automatic token handling in API requests

### Expense Management
- Add new expenses with title, amount, category, date, and notes
- View all expenses with category filtering
- Edit existing expenses
- Delete expenses
- Predefined categories: Food, Travel, Shopping, Bills, Entertainment, Other

### Dashboard
- Total expenses overview
- Current month spending summary
- Category-wise expense breakdown with percentages
- Monthly expense trends (last 12 months)

## Application Flow

1. **Register**: Create a new account at `/register`
2. **Login**: Sign in at `/login` to receive JWT token
3. **Dashboard**: View expense statistics at `/dashboard`
4. **Manage Expenses**: Add, edit, and delete expenses at `/expenses`

## API Documentation

Complete API documentation is available in `API_DOCUMENTATION.md` or at `http://localhost:8000/docs`

## Development Phases (All Completed)

✅ **Phase 1**: Project Setup, MySQL Configuration, FastAPI Setup
✅ **Phase 2**: User Authentication (Registration, Login, JWT)
✅ **Phase 3**: Expense CRUD Operations
✅ **Phase 4**: Dashboard APIs
✅ **Phase 5**: React Frontend Integration

## Security Notes

- Passwords are hashed using bcrypt before storage
- JWT tokens expire after 30 minutes (configurable)
- All expense endpoints require authentication
- Users can only access their own expenses
- Never commit `.env` file to version control
