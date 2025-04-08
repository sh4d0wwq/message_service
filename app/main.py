from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.message import router as message_router
from app.db.database import engine, Base
from app.middleware.jwt_middleware import JWTMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    description="Микросервис аутентификации на FastAPI",
    version="1.0.0",
)

app.add_middleware(JWTMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router)