from .db.database import SessionLocal
from fastapi import Request, Depends
from .services.message_service import MessageService
from .services.chat_service import ChatService
from .repositories.message_repository import MessageRepository
from .repositories.chat_repository import ChatRepository
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(request: Request):
    return request.state.user_id

def get_message_service(db: Session = Depends(get_db)):
    return MessageService(MessageRepository(db))

def get_chat_service(db: Session = Depends(get_db)):
    return ChatService(ChatRepository(db))
