# Telco CRM - Customer Relationship Management System

A comprehensive CRM application for managing Telco customers with machine learning-powered churn prediction, built with FastAPI, React, and MySQL.

## 🎯 Features

### Core CRM Functionality
- **User Management**: Create, edit, and manage staff accounts with role-based access control
- **Customer Management**: Complete customer database with 33 data fields
- **Churn Prediction**: ML-powered prediction of customer churn probability
- **Dashboard**: Real-time analytics and KPI monitoring
- **Audit Trail**: Comprehensive logging of all system activities

### Security & RBAC
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Three roles (Admin, Manager, Staff) with granular permissions
- **Password Hashing**: bcrypt-based password security
- **Session Management**: Automatic logout on token expiry

### ML & Analytics
- **Random Forest Model**: Real-time churn scoring
- **Predictions**: Evaluate customer churn risk before assignment
- **Analytics**: Contract type churn analysis, revenue tracking
- **Model Retraining**: Support for updating ML model with new data

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Docker & Docker Compose (optional)

## 🚀 Quick Start

### Option 1: Local Development Setup

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate Python virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create MySQL database**:
   ```bash
   mysql -u root -p
   CREATE DATABASE telco_crm;
   EXIT;
   ```

5. **Configure environment variables**:
   ```bash
   # Copy .env.example to .env
   cp .env.example .env
   
   # Edit .env with your configuration
   nano .env
   ```

6. **Start the backend server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

Backend will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   ```bash
   # Copy .env.example to .env
   cp .env.example .env
   
   # Edit .env if needed (default points to localhost:8000)
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

Frontend will be available at: `http://localhost:5173`

### Option 2: Docker Compose Setup

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- MySQL: `localhost:3306`

## 🔑 Default Credentials

```
Username: admin
Password: admin123
```

⚠️ **IMPORTANT**: Change these credentials in production!

## 📁 Project Structure

```
telco-crm/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/              # API Endpoints
│   │   │   │   ├── auth.py          # Authentication
│   │   │   │   ├── users.py         # User Management
│   │   │   │   ├── customers.py     # Customer CRUD
│   │   │   │   ├── predict.py       # ML Predictions
│   │   │   │   └── dashboard.py     # Analytics
│   │   │   └── dependencies.py      # Auth middleware
│   │   ├── core/
│   │   │   ├── config.py            # Configuration
│   │   │   └── security.py          # JWT & Hashing
│   │   ├── crud/                    # Database Operations
│   │   ├── models/                  # SQLAlchemy Models
│   │   ├── schemas/                 # Pydantic Schemas
│   │   ├── services/                # Business Logic
│   │   ├── db/                      # Database Setup
│   │   └── main.py                  # Application Entry
│   ├── ml_models/                   # Trained Models
│   ├── requirements.txt             # Dependencies
│   ├── .env.example                 # Environment Template
│   └── Dockerfile                   # Container Config
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Auth/                # Login Page
│   │   │   ├── Dashboard/           # Analytics Dashboard
│   │   │   ├── Customers/           # Customer Pages
│   │   │   ├── Users/               # User Management
│   │   │   ├── Profile/             # Profile & Security
│   │   │   └── Unauthorized.jsx     # 403 Page
│   │   ├── services/                # API Clients
│   │   │   ├── authApi.js
│   │   │   ├── userApi.js
│   │   │   ├── customerApi.js
│   │   │   ├── dashboardApi.js
│   │   │   └── axiosClient.js
│   │   ├── components/              # React Components
│   │   │   ├── Layout.jsx           # Main Layout
│   │   │   └── ProtectedRoute.jsx   # Route Guards
│   │   ├── context/                 # Auth Context
│   │   ├── App.jsx                  # Main App
│   │   └── main.jsx                 # Entry Point
│   ├── package.json                 # Dependencies
│   ├── .env.example                 # Environment Template
│   ├── Dockerfile                   # Container Config
│   └── vite.config.js               # Build Config
│
├── scripts/
│   └── train_model.py               # ML Training Script
│
├── docker-compose.yml               # Multi-container Setup
├── .gitignore                        # Git Ignore Rules
└── README.md                         # This File
```

## 🔐 User Roles & Permissions

### Admin
- Access all features
- Create/manage users
- Manage customer records
- View all analytics
- Activate/deactivate accounts

### Manager
- View customer records
- Create customer records
- View staff list (Staff only)
- View analytics
- Change own password

### Staff
- View assigned customers
- View own profile
- Change own password
- Access dashboard

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Users
- `GET /api/users/` - List users (Admin/Manager)
- `POST /api/users/` - Create user (Admin)
- `GET /api/users/{id}` - Get user details
- `PATCH /api/users/{id}/status` - Update user status (Admin)
- `PUT /api/users/me/password` - Change password

### Customers
- `GET /api/customers/` - List customers with filters
- `POST /api/customers/` - Create customer
- `GET /api/customers/{id}` - Get customer details
- `PUT /api/customers/{id}` - Update customer
- `PATCH /api/customers/{id}/churn` - Mark customer as churned

### Predictions
- `POST /api/predict/evaluate` - Get churn prediction

### Dashboard
- `GET /api/dashboard/summary` - Get KPI summary
- `GET /api/dashboard/charts/churn-by-contract` - Get chart data

## 🤖 Machine Learning

### Training Model with Real Data

```bash
# Using the training script
python scripts/train_model.py --data /path/to/telco_data.csv --output ml_models/random_forest_churn.pkl

# With custom parameters
python scripts/train_model.py \
  --data telco_data.csv \
  --output ml_models/model.pkl \
  --estimators 150 \
  --test-size 0.2
```

### Input Data Format

The training script expects CSV with these columns:
- `tenure_months` (int)
- `monthly_charges` (float)
- `total_charges` (float)
- `partner` ('Yes'/'No')
- `dependents` ('Yes'/'No')
- `contract` ('Month-to-month'/'One year'/'Two year')
- `internet_service` ('DSL'/'Fiber optic'/'No')
- `paperless_billing` ('Yes'/'No')
- `churn_label` or `Churn` ('Yes'/'No') - Target variable

## 🛠️ Environment Variables

### Backend (.env)

```env
# Database
MYSQL_URL=mysql+pymysql://root:@localhost:3306/telco_crm

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Default Admin
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=admin123

# API
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Telco CRM
VITE_APP_VERSION=1.0.0
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Build

```bash
cd frontend
npm run build
```

## 📝 Logging

All system activities are logged including:
- User login/logout
- User creation and status changes
- Customer operations (CRUD)
- Churn predictions
- Password changes
- Failed authentication attempts
- Permission violations

Logs are output to console (configure in backend config).

## 🐛 Troubleshooting

### Database Connection Error
```
Error: Can't connect to MySQL server
```
- Ensure MySQL is running
- Verify connection string in .env
- Check database exists: `SHOW DATABASES;`

### Port Already in Use
```
Address already in use
```
- Backend (8000): `lsof -i :8000` then `kill -9 <PID>`
- Frontend (5173): `lsof -i :5173` then `kill -9 <PID>`

### Module Not Found
```
ModuleNotFoundError: No module named 'fastapi'
```
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```
- Check VITE_API_URL in frontend .env
- Verify backend CORS configuration

## 🚢 Deployment

### Using Docker
```bash
docker-compose up -d
```

### Environment Setup
1. Generate strong SECRET_KEY
2. Set all .env variables for production
3. Enable HTTPS in production
4. Configure database backups
5. Set up monitoring and alerting

## 📄 License

This project is confidential and proprietary.

## 👥 Support

For issues and questions, contact the development team.
