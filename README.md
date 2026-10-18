# 💸 Finance & Subscription Tracker Microservice


A high-performance, asynchronous RESTful microservice built with **FastAPI**, **SQLAlchemy ORM**, and **Alembic**. It provides complete management for personal expenses, recurring subscription tracking, real-time analytics aggregation, CSV data exports, and secure user authentication via JWT bearer tokens.

---

## 🚀 Key Features

* **Authentication & Security:**
  * User registration and login flows (`/auth/register`, `/auth/login`).
  * Secure password hashing with Argon2 / Pwdlib.
  * Stateless JWT access token generation and authentication dependencies (`/auth/me`).

* **Expense Management (CRUD):**
  * Full create, read, update, and delete support with strict validation via Pydantic schemas.
  * Query parameters for filtering by category, date ranges, and pagination (`skip`, `limit`).
  * On-the-fly streaming export of filtered expenses directly to **CSV** (`/expenses/export`).

* **Subscription Tracking:**
  * Model recurring monthly and yearly payments (e.g., Netflix, Spotify).
  * Status monitoring (`active`, `canceled`) and tracking of upcoming billing cycles (`next_billing_date`).

* **Analytics & Reporting:**
  * Real-time metrics calculation (`total_spent`, `average_expense_amount`, total transactions).
  * Grouped aggregations per expense category using SQL aggregation functions.

* **Database Version Control:**
  * Integrated **Alembic** migrations tracking schema evolutions with zero data loss.

---

## 🏗️ Project Architecture

```text
Backend.Microservice.FastAPI.PostgreSQL/
├── alembic/                      # Alembic migration scripts and env configuration
│   ├── versions/                 # Individual database revision files
│   └── env.py                    # Migration execution environment
├── src/
│   ├── models/                   # SQLAlchemy database models
│   │   ├── expense.py
│   │   ├── subscription.py
│   │   └── user.py
│   ├── schemas/                  # Pydantic schemas for request/response validation
│   │   ├── expense.py
│   │   ├── subscription.py
│   │   ├── analytics.py
│   │   └── user.py
│   ├── routers/                  # API endpoints organized by domain
│   │   ├── auth.py
│   │   ├── expenses.py
│   │   ├── subscriptions.py
│   │   └── analytics.py
│   ├── auth_utils.py             # Password hashing and JWT generation routines
│   ├── database.py               # Engine setup, sessionmaker, and Base definition
│   ├── dependencies.py           # Dependency injection (e.g., get_current_user)
│   └── main.py                   # FastAPI initialization & router registration
├── .gitignore                    # Git ignore file (excludes .venv, databases, caches)
├── alembic.ini                   # Alembic runtime settings
├── requirements.txt              # Production and development dependencies
└── README.md                     # Project documentation
```

---

## 🛠️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/tsothsss/finance-tracker-api.git
cd finance-tracker-api
```

### 2. Set Up a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Apply Database Migrations
Initialize and upgrade your database tables using Alembic:
```bash
alembic upgrade head
```

### 5. Launch the Application
```bash
uvicorn src.main:app --reload
```
The server will be available at `http://127.0.0.1:8000`.

---

## 📖 API Documentation & Endpoints

FastAPI automatically generates interactive API documentation. Once the server is running, visit:
* **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Interface:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Summary of Endpoints

| Tag | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Health** | `GET` | `/` | Service health status check |
| **Auth** | `POST` | `/auth/register` | Register a new user |
| **Auth** | `POST` | `/auth/login` | Authenticate user and obtain JWT token |
| **Auth** | `GET` | `/auth/me` | Fetch authenticated user details |
| **Expenses** | `GET` | `/expenses/` | List expenses with filtering & pagination |
| **Expenses** | `POST` | `/expenses/` | Create a new expense |
| **Expenses** | `GET` | `/expenses/export` | Download expenses as a `.csv` file |
| **Expenses** | `GET` | `/expenses/{id}` | Retrieve expense details by ID |
| **Expenses** | `PUT` | `/expenses/{id}` | Update an existing expense record |
| **Expenses** | `DELETE`| `/expenses/{id}` | Delete an expense record |
| **Subscriptions** | `GET` | `/subscriptions/` | List all tracked recurring subscriptions |
| **Subscriptions** | `POST` | `/subscriptions/` | Register a new recurring subscription |
| **Subscriptions** | `DELETE`| `/subscriptions/{id}` | Remove a subscription |
| **Analytics** | `GET` | `/analytics/summary` | Get aggregated financial summary & stats |

---

## 🔒 Environment & Configuration

To adapt this service for production using PostgreSQL:
1. Update `alembic.ini` and `src/database.py` with your PostgreSQL connection URI:
   ```text
   postgresql+psycopg2://<user>:<password>@<host>:<port>/<dbname>
   ```
2. Store critical settings such as `SECRET_KEY` inside environment variables or `.env` files.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
