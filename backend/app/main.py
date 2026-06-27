import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, customers, dashboard, predict, users
from app.core.config import settings
from app.core.security import get_password_hash
from app.crud.crud_user import get_user_by_username
from app.db.base import Base
from app.db.database import SessionLocal, engine
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Telco CRM")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(predict.router)
app.include_router(dashboard.router)
app.include_router(users.router)


@app.on_event("startup")
def startup_event() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            if not get_user_by_username(db, settings.DEFAULT_ADMIN_USERNAME):
                admin = User(
                    username=settings.DEFAULT_ADMIN_USERNAME,
                    email="admin@telco.local",
                    full_name="System Administrator",
                    hashed_password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
                    role="admin",
                    is_active=True,
                )
                db.add(admin)
                db.commit()
        finally:
            db.close()
    except Exception as exc:
        logger.warning("Database initialization skipped: %s", exc)


@app.get("/health")
def health_check():
    return {"status": "ok"}
