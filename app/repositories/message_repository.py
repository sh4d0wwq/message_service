from sqlalchemy.orm import Session
from ..models.message import Message
from ..models.chat import Chat
from ..schemas.base_models import MessageCreate
from typing import List

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, sender_id: int, message: MessageCreate) -> Message:
        db_message = Message(sender_id = sender_id, chat_id = message.chat_id, content = message.content, attachment_url = message.attachment_url)
        
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)

        chat = self.db.query(Chat).where(Chat.chat_id == db_message.chat_id).first()
        chat.last_message = db_message.id

        self.db.commit()
        self.db.refresh(chat)

        return db_message
    
    def get_messages(self, chat_id: int, limit: int, offset: int) -> List[Message] | None:
        return self.db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.timestamp.desc()).offset(offset).limit(limit).all()
        