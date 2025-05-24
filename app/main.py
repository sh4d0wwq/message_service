from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.message import router as message_router
from app.db.database import engine, Base
from app.middleware.jwt_middleware import JWTMiddleware
from app.api.ws import router as chat_ws_handler_router 

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Message Service",
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

app.include_router(chat_ws_handler_router)