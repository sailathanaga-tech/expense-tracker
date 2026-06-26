# API Documentation

## Authentication Endpoints (Phase 2)

### 1. Register User

**Endpoint:** `POST /api/auth/register`

**Description:** Register a new user account.

**Request Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Request Schema:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| username | string | 3-50 characters, required | Unique username for login |
| email | string | Valid email format, required | User's email address |
| password | string | Minimum 6 characters, required | User's password |

**Success Response (201 Created):**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

**Error Responses:**

**400 Bad Request - Username already exists:**

```json
{
  "detail": "Username already registered"
}
```

**400 Bad Request - Email already exists:**

```json
{
  "detail": "Email already registered"
}
```

**422 Unprocessable Entity - Validation error:**

```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "ensure this value has at least 3 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

### 2. Login User

**Endpoint:** `POST /api/auth/login`

**Description:** Login with username/email and password to receive JWT token.

**Request Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "username_or_email": "john_doe",
  "password": "securepassword123"
}
```

**Request Schema:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| username_or_email | string | Required | Username or email address |
| password | string | Required | User's password |

**Success Response (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**

**401 Unauthorized - Invalid credentials:**

```json
{
  "detail": "Invalid credentials"
}
```

**422 Unprocessable Entity - Validation error:**

```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## JWT Token Usage

### How to Use the Token

After successful login, include the token in the Authorization header for protected routes:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Payload Structure

The JWT token contains the following payload:

```json
{
  "user_id": 1,
  "exp": 1705349400,
  "iat": 1705347600
}
```

| Field   | Description                                 |
| ------- | ------------------------------------------- |
| user_id | The authenticated user's ID                 |
| exp     | Token expiration timestamp (Unix timestamp) |
| iat     | Token issued at timestamp (Unix timestamp)  |

### Token Expiration

- Default expiration: 30 minutes
- Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env` file

---

## Testing with cURL

### Register a new user:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Login:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "testuser",
    "password": "password123"
  }'
```

### Access protected route (example):

```bash
curl -X GET http://localhost:8000/api/expenses \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Testing with Swagger UI

1. Start the FastAPI server: `python -m uvicorn app.main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Click on `/api/auth/register` → Try it out
4. Fill in the request body and execute
5. Copy the response data
6. Click on `/api/auth/login` → Try it out
7. Fill in the request body and execute
8. Copy the `access_token` from the response
9. Use the token in the Authorize button (top right) for protected routes

---

## Expense Endpoints (Phase 3)

**Note:** All expense endpoints require authentication. Include the JWT token in the Authorization header.

### 1. Create Expense

**Endpoint:** `POST /api/expenses/`

**Description:** Create a new expense for the authenticated user.

**Request Headers:**

```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN_HERE
```

**Request Body:**

```json
{
  "title": "Grocery shopping",
  "amount": 150.5,
  "category": "Food",
  "date": "2024-01-15T10:30:00",
  "notes": "Weekly groceries"
}
```

**Request Schema:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| title | string | 1-200 characters, required | Expense title |
| amount | float | Must be positive, required | Expense amount |
| category | string | Required, must be one of predefined categories | Expense category |
| date | datetime | Required | Date of expense |
| notes | string | Optional, max 500 characters | Additional notes |

**Valid Categories:** Food, Travel, Shopping, Bills, Entertainment, Other

**Success Response (201 Created):**

```json
{
  "id": 1,
  "title": "Grocery shopping",
  "amount": 150.5,
  "category": "Food",
  "date": "2024-01-15T10:30:00",
  "notes": "Weekly groceries",
  "user_id": 1,
  "created_at": "2024-01-15T10:30:00"
}
```

**Error Responses:**

**401 Unauthorized:** Invalid or missing token

**422 Unprocessable Entity - Invalid category:**

```json
{
  "detail": [
    {
      "loc": ["body", "category"],
      "msg": "Invalid category. Must be one of: Food, Travel, Shopping, Bills, Entertainment, Other",
      "type": "value_error"
    }
  ]
}
```

---

### 2. Get All Expenses

**Endpoint:** `GET /api/expenses/`

**Description:** Get all expenses for the authenticated user. Supports filtering by category and pagination.

**Request Headers:**

```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| category | string | None | Filter by category |
| skip | integer | 0 | Number of expenses to skip (pagination) |
| limit | integer | 100 | Maximum number of expenses to return (1-100) |

**Example:** `GET /api/expenses/?category=Food&skip=0&limit=10`

**Success Response (200 OK):**

```json
{
  "expenses": [
    {
      "id": 1,
      "title": "Grocery shopping",
      "amount": 150.5,
      "category": "Food",
      "date": "2024-01-15T10:30:00",
      "notes": "Weekly groceries",
      "user_id": 1,
      "created_at": "2024-01-15T10:30:00"
    },
    {
      "id": 2,
      "title": "Bus ticket",
      "amount": 5.0,
      "category": "Travel",
      "date": "2024-01-14T08:00:00",
      "notes": null,
      "user_id": 1,
      "created_at": "2024-01-14T08:00:00"
    }
  ],
  "total": 2
}
```

**Error Responses:**

**401 Unauthorized:** Invalid or missing token

---

### 3. Get Single Expense

**Endpoint:** `GET /api/expenses/{expense_id}`

**Description:** Get a single expense by ID.

**Request Headers:**

```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| expense_id | integer | ID of the expense |

**Success Response (200 OK):**

```json
{
  "id": 1,
  "title": "Grocery shopping",
  "amount": 150.5,
  "category": "Food",
  "date": "2024-01-15T10:30:00",
  "notes": "Weekly groceries",
  "user_id": 1,
  "created_at": "2024-01-15T10:30:00"
}
```

**Error Responses:**

**401 Unauthorized:** Invalid or missing token

**403 Forbidden:** Expense belongs to another user

```json
{
  "detail": "You don't have permission to access this expense"
}
```

**404 Not Found:** Expense doesn't exist

```json
{
  "detail": "Expense not found"
}
```

---

### 4. Update Expense

**Endpoint:** `PUT /api/expenses/{expense_id}`

**Description:** Update an existing expense. Only provided fields will be updated.

**Request Headers:**

```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN_HERE
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| expense_id | integer | ID of the expense |

**Request Body (all fields optional):**

```json
{
  "title": "Grocery shopping - updated",
  "amount": 200.0,
  "category": "Food",
  "date": "2024-01-15T10:30:00",
  "notes": "Monthly groceries"
}
```

**Success Response (200 OK):**

```json
{
  "id": 1,
  "title": "Grocery shopping - updated",
  "amount": 200.0,
  "category": "Food",
  "date": "2024-01-15T10:30:00",
  "notes": "Monthly groceries",
  "user_id": 1,
  "created_at": "2024-01-15T10:30:00"
}
```

**Error Responses:**

**401 Unauthorized:** Invalid or missing token

**403 Forbidden:** Expense belongs to another user

**404 Not Found:** Expense doesn't exist

**422 Unprocessable Entity:** Invalid data

---

### 5. Delete Expense

**Endpoint:** `DELETE /api/expenses/{expense_id}`

**Description:** Delete an expense.

**Request Headers:**

```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| expense_id | integer | ID of the expense |

**Success Response (204 No Content):**
No response body

**Error Responses:**

**401 Unauthorized:** Invalid or missing token

**403 Forbidden:** Expense belongs to another user

**404 Not Found:** Expense doesn't exist

---

## Testing Expense Endpoints with cURL

### Create expense:

```bash
curl -X POST http://localhost:8000/api/expenses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Grocery shopping",
    "amount": 150.50,
    "category": "Food",
    "date": "2024-01-15T10:30:00",
    "notes": "Weekly groceries"
  }'
```

### Get all expenses:

```bash
curl -X GET http://localhost:8000/api/expenses/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get expenses filtered by category:

```bash
curl -X GET "http://localhost:8000/api/expenses/?category=Food" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get single expense:

```bash
curl -X GET http://localhost:8000/api/expenses/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Update expense:

```bash
curl -X PUT http://localhost:8000/api/expenses/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Grocery shopping - updated",
    "amount": 200.0
  }'
```

### Delete expense:

```bash
curl -X DELETE http://localhost:8000/api/expenses/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Dashboard Endpoints (Phase 4)

**Note:** Dashboard endpoints require authentication. Include the JWT token in the Authorization header.

### 1. Get Dashboard Summary

**Endpoint:** `GET /api/dashboard/summary`

**Description:** Get complete dashboard summary including total expenses, category-wise breakdown, and monthly trends.

**Request Headers:**

```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Success Response (200 OK):**

```json
{
  "total_expenses": 1250.75,
  "total_expense_count": 15,
  "category_summary": [
    {
      "category": "Food",
      "total_amount": 500.5,
      "expense_count": 8,
      "percentage": 40.02
    },
    {
      "category": "Travel",
      "total_amount": 300.25,
      "expense_count": 3,
      "percentage": 24.01
    },
    {
      "category": "Shopping",
      "total_amount": 250.0,
      "expense_count": 2,
      "percentage": 20.0
    },
    {
      "category": "Bills",
      "total_amount": 150.0,
      "expense_count": 1,
      "percentage": 12.0
    },
    {
      "category": "Entertainment",
      "total_amount": 50.0,
      "expense_count": 1,
      "percentage": 4.0
    }
  ],
  "monthly_expenses": [
    {
      "month": "2024-01",
      "total_amount": 800.5,
      "expense_count": 10
    },
    {
      "month": "2023-12",
      "total_amount": 450.25,
      "expense_count": 5
    }
  ],
  "current_month_total": 800.5,
  "current_month_count": 10
}
```

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| total_expenses | float | Sum of all expense amounts |
| total_expense_count | integer | Total number of expenses |
| category_summary | array | List of category-wise summaries |
| monthly_expenses | array | List of monthly expense summaries (last 12 months) |
| current_month_total | float | Total expenses for current month |
| current_month_count | integer | Number of expenses in current month |

**Category Summary Schema:**

| Field | Type | Description |
|-------|------|-------------|
| category | string | Category name |
| total_amount | float | Total amount for this category |
| expense_count | integer | Number of expenses in this category |
| percentage | float | Percentage of total expenses |

**Monthly Expense Schema:**

| Field | Type | Description |
|-------|------|-------------|
| month | string | Month in "YYYY-MM" format |
| total_amount | float | Total amount for this month |
| expense_count | integer | Number of expenses in this month |

**Error Responses:**

**401 Unauthorized:** Invalid or missing token

---

## Testing Dashboard Endpoint with cURL

### Get dashboard summary:

```bash
curl -X GET http://localhost:8000/api/dashboard/summary \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
