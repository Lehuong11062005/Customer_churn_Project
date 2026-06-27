# Telco CRM

## Backend

1. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
2. Start the API server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Frontend

1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the Vite app:
   ```bash
   npm run dev
   ```

## Database

- Create a MySQL database named `telco_crm`.
- The backend will create tables automatically on startup.
