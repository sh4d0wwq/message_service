from .db.database import SessionLocal
from fastapi import Request, Depends, WebSocket, HTTPException, status
from .services.message_service import MessageService
from .services.chat_service import ChatService
from .services.chat_user_service import ChatUserService
from jose import jwt, JWTError
from .config import Config
from .repositories.message_repository import MessageRepository
from .repositories.chat_repository import ChatRepository
from .repositories.chat_user_repository import ChatUserRepository
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(request: Request) -> str:
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user_id

def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(MessageRepository(db))

def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    return ChatService(ChatRepository(db), ChatUserRepository(db))

def get_chat_user_service(db: Session = Depends(get_db)) -> ChatUserService:
    return ChatUserService(ChatUserRepository(db))

async def get_current_ws_user_id(websocket: WebSocket) -> int:
    token = websocket.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=403, detail="Missing token")

    try:
        payload = jwt.decode(token, Config.ACCESS_SECRET_KEY, algorithms=["HS256"])
        return int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")