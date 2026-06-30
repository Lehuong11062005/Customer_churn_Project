import logging
import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, customers, dashboard, predict, users
from app.core.config import settings
from app.core.security import get_password_hash
from app.crud.crud_user import get_user_by_username
from app.db.base import Base
from app.db.database import SessionLocal, engine
from app.models.user import User
from app.api.routes import model_performance
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Telco CRM")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173",
                   "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(predict.router)
app.include_router(dashboard.router)
app.include_router(users.router)
app.include_router(model_performance.router)

@app.on_event("startup")
def startup_event() -> None:
    try:
        logger.info("Starting Telco CRM application...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
        
        db = SessionLocal()
        try:
            if not get_user_by_username(db, settings.DEFAULT_ADMIN_USERNAME):
                admin = User(
                    username=settings.DEFAULT_ADMIN_USERNAME,
                    email="admin@telco.com",
                    full_name="System Administrator",
                    hashed_password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
                    role="admin",
                    is_active=True,
                )
                db.add(admin)
                db.commit()
                logger.info(f"Default admin user created: {settings.DEFAULT_ADMIN_USERNAME}")
            else:
                logger.debug("Admin user already exists")
        finally:
            db.close()
        
        logger.info("Telco CRM application ready!")
    except Exception as exc:
        logger.error(f"Error during startup: {exc}", exc_info=True)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "telco-crm"}
