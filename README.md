
Finance Tracker API
A FastAPI backend for recording expenses, keeping track of subscriptions, and seeing where your money goes. It includes expense filtering, CSV exports, spending summaries, and a registration and login flow.

The app uses SQLite for local storage, synchronous SQLAlchemy sessions for database access, and Alembic for schema migrations.

What it does
Create, list, edit, and delete expenses.
Filter expenses by category and date range, with pagination.
Export filtered expenses to CSV.
Store monthly or yearly subscriptions with a billing date and status.
Calculate total spending, expense count, average expense amount, and totals by category.
Register users, hash passwords with Argon2 through pwdlib, and issue JWT access tokens.
Current scope: only GET /auth/me requires authentication. Expense, subscription, export, and analytics endpoints are public, and records are not linked to individual users. Use the current version locally with sample data.

Run locally
You need Python, pip, and Git. The repository does not declare a supported Python version; dependency versions are pinned in requirements.txt.

1. Clone the repository
git clone https://github.com/tsothsss/finance-tracker-api.git
cd finance-tracker-api
Run the remaining commands from this directory so the app and Alembic use the same SQLite database file.

2. Create a virtual environment
macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate
Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
4. Set up the database
python -m alembic upgrade head
This creates finance.db in the project directory and applies the migrations.

Fresh-database workaround: the initial expenses migration currently has an empty upgrade(), so it does not create the expenses table. After running Alembic, create that table from the existing model:

python -c "from src.database import engine; from src.models.expense import ExpenseModel; ExpenseModel.__table__.create(bind=engine, checkfirst=True)"
This is a local setup workaround until the migration is fixed. It creates the table only if it is missing; it does not migrate an existing table.

5. Start the server
python -m uvicorn src.main:app --reload
Open:

Service status
Swagger UI to try requests in the browser
ReDoc for the API reference
The root endpoint returns:

{
  "status": "online",
  "service": "Finance Tracker API",
  "version": "1.0.0"
}
Try the API
These examples use Bash-style shell syntax and curl. On Windows, you can use Git Bash or send the same requests through Swagger UI.

Record an expense
curl -X POST http://127.0.0.1:8000/expenses/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weekly groceries",
    "amount": 42.50,
    "category": "food",
    "expense_date": "2026-11-02",
    "notes": "Supermarket"
  }'
The response includes the saved expense and its id. Amounts must be positive. If omitted, category defaults to other and expense_date defaults to the current date.

Allowed categories: food, housing, entertainment, transport, utilities, subscription, and other.

Filter expenses and export CSV
curl "http://127.0.0.1:8000/expenses/?category=food&start_date=2026-11-01&end_date=2026-11-30&skip=0&limit=20"

curl "http://127.0.0.1:8000/expenses/export?start_date=2026-11-01&end_date=2026-11-30" \
  -o expenses.csv
Date boundaries are inclusive. The list endpoint defaults to skip=0 and limit=20, with a maximum limit of 100. CSV export includes all matching expenses, sorted by date from newest to oldest.

Add a subscription
curl -X POST http://127.0.0.1:8000/subscriptions/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Music subscription",
    "amount": 7.99,
    "billing_cycle": "monthly",
    "next_billing_date": "2026-12-02",
    "status": "active"
  }'
Billing cycles are monthly or yearly; statuses are active or canceled. Subscriptions store billing information. They do not charge payments, advance billing dates, or automatically create expenses.

View a spending summary
curl "http://127.0.0.1:8000/analytics/summary?start_date=2026-11-01&end_date=2026-11-30"
With only the groceries expense above in that period, the response is:

{
  "total_spent": 42.5,
  "total_expenses_count": 1,
  "average_expense_amount": 42.5,
  "by_category": {
    "food": 42.5
  }
}
Analytics are calculated from expenses only. Subscription amounts are not included.

Register and log in
Registration accepts JSON:

curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "email": "demo@example.com",
    "password": "local-demo-password"
  }'
Login accepts form data and uses the username, not the email:

curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "username=demo" \
  --data-urlencode "password=local-demo-password"
Copy the returned access_token, then use it to fetch your profile:

read -r -s -p "Paste access_token: " TOKEN
printf '\n'
curl http://127.0.0.1:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
unset TOKEN
Tokens expire after 60 minutes. In Swagger UI, click Authorize and enter the registered username and password to test /auth/me.

Endpoints
Method	Path	Purpose	Token required
GET	/	Service status	No
POST	/auth/register	Register a user	No
POST	/auth/login	Get a JWT access token	No
GET	/auth/me	Get the authenticated user's profile	Yes
GET	/expenses/	List and filter expenses	No
POST	/expenses/	Create an expense	No
GET	/expenses/export	Export filtered expenses to CSV	No
GET	/expenses/{expense_id}	Get one expense	No
PUT	/expenses/{expense_id}	Update supplied expense fields	No
DELETE	/expenses/{expense_id}	Delete an expense	No
GET	/subscriptions/	List subscriptions	No
POST	/subscriptions/	Create a subscription	No
DELETE	/subscriptions/{sub_id}	Delete a subscription	No
GET	/analytics/summary	Summarize expenses, optionally by date range	No
The expense update endpoint accepts partial field updates despite using PUT. There is no subscription update endpoint yet.

Create requests return 201; successful deletes return 204 without a response body. Missing expense or subscription IDs return 404. Invalid request fields normally return 422.

Code layout
Path	Responsibility
main.py
App configuration, router registration, and service status
Authentication, expenses, subscriptions, and analytics endpoints
SQLAlchemy database models
Pydantic request and response schemas
database.py
SQLite engine and database sessions
auth_utils.py
Password hashing and token creation
dependencies.py
Bearer token validation and current-user lookup
Database migrations
alembic.ini
Alembic configuration and database URL
Configuration and current limitations
Both src/database.py and alembic.ini use sqlite:///./finance.db. No external database server is needed for local use.

Settings are currently defined in code. Adding a .env file alone will not change the database URL or JWT secret because the application does not load those values from the environment.

Before using this with real financial data:

Replace the hard-coded JWT development secret with a secret loaded from configuration.
Add authentication and per-user ownership checks to financial endpoints. The current data is shared across all callers.
Fix the empty expenses migration so a fresh database can be initialized through Alembic alone.
Review monetary storage: amounts currently use floating-point values, and the API has no currency field. CSV headers label amounts in euros.
Switching to PostgreSQL also requires installing a database driver, updating both database URLs, and removing the SQLite-specific check_same_thread connection argument.

The repository does not currently include an automated test suite or a license file.

90 ms
