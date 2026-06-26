"""
FastAPI Application Entry Point

This is the main file that initializes the FastAPI application.
It sets up CORS, includes routers, and defines the root endpoint.

Why this file exists:
- Entry point for the application
- Central place to configure the app
- Includes all route modules
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.config import engine, Base
from app.routes import auth, expenses, dashboard

# Create FastAPI application instance
app = FastAPI(
    title="Expense Tracker API",
    description="A simple expense tracker application with user authentication",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows the React frontend to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers from different modules
# This organizes routes into logical groups
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["Expenses"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])


# Root endpoint
@app.get("/")
def root():
    """Root endpoint to check if the API is running"""
    return {"message": "Expense Tracker API is running"}


# Create database tables on startup
# This is a simple approach - in production, use Alembic migrations
@app.on_event("startup")
def startup_event():
    """Create all database tables on application startup"""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
