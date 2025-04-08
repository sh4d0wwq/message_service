import os

class Config:
    ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY", "FuckThePopulation")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "ShitHappens")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30 
    REFRESH_TOKEN_EXPIRE_DAYS = 30
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Password1065@localhost/message_db"
    )