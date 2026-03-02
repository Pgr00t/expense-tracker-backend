# Expense Tracker Backend (Django)

## Prerequisites
- Python 3.9+
- pip

## Local Setup

1. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run Database Migrations:
   ```bash
   python manage.py migrate
   ```

4. Start Local Server:
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000/api/expenses/`.

## Endpoints

- `GET /api/expenses/` - List all expenses
- `POST /api/expenses/` - Create a new expense
- `GET /api/expenses/<id>/` - Retrieve an expense
- `PUT /api/expenses/<id>/` - Update an expense
- `DELETE /api/expenses/<id>/` - Delete an expense
- `GET /api/expenses/summary/` - Get total spent & category breakdown
- `GET /api/expenses/convert_currency/?amount=<amount>&from=<base>&to=<target>` - Live currency conversion (Third-Party API Integration)

## Third-Party API
We use the [Frankfurter API](https://api.frankfurter.app/) to fetch real-time exchange rates to show current expenses in other global currencies. This is integrated in the `convert_currency` endpoint.
