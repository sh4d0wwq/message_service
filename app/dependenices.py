from .db.database import SessionLocal
from fastapi import Request, Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(request: Request):
    return request.state.user_id