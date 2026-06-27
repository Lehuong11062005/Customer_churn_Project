import os


class Settings:
    MYSQL_URL = os.getenv("MYSQL_URL", "mysql+pymysql://root:@localhost:3306/telco_crm")
    SECRET_KEY = os.getenv("SECRET_KEY", "telco-crm-secret-key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    DEFAULT_ADMIN_USERNAME = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
    DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")


settings = Settings()
