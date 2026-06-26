# Database Design for Expense Tracker

## ER Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │───┐
│ username        │   │
│ email           │   │
│ hashed_password │   │
│ created_at      │   │
└─────────────────┘   │
                      │
                      │ 1
                      │
                      │ N
                      │
┌─────────────────┐   │
│   expenses      │◄──┘
├─────────────────┤
│ id (PK)         │
│ title           │
│ amount          │
│ category        │
│ date            │
│ notes           │
│ user_id (FK)    │
│ created_at      │
└─────────────────┘
```

## Table Structure

### users table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT, INDEX | Unique user identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | User's login name |
| email | VARCHAR(100) | UNIQUE, NOT NULL, INDEX | User's email address |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

### expenses table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT, INDEX | Unique expense identifier |
| title | VARCHAR(200) | NOT NULL | Short description of expense |
| amount | FLOAT | NOT NULL | Expense amount |
| category | VARCHAR(50) | NOT NULL | Category (Food, Travel, Shopping, etc.) |
| date | DATETIME | NOT NULL | Date when expense occurred |
| notes | VARCHAR(500) | NULL | Additional notes |
| user_id | INT | NOT NULL, FOREIGN KEY → users.id | Reference to user |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Expense creation timestamp |

## Relationships

- **One-to-Many**: One user can have many expenses
- **Foreign Key**: expenses.user_id references users.id
- **Cascade**: When a user is deleted, their expenses are also deleted

## SQL Create Table Queries

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS expense_tracker;
USE expense_tracker;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Create expenses table
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    date DATETIME NOT NULL,
    notes VARCHAR(500),
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_date (date),
    INDEX idx_category (category)
);
```

## Predefined Categories

The following categories are predefined in the application:

1. Food
2. Travel
3. Shopping
4. Bills
5. Entertainment
6. Other

These will be validated at the application level (in Pydantic schemas).
