from sqlalchemy.orm import Session
from ..models.message import Message, MessageCreate

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, sender_id: int, message: MessageCreate) -> Message:
        db_message = Message(sender_id = sender_id, chat_id = message.chat_id, content = message.content)
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
    
    def get_messages(self, user_id: int, contact_id: int):
        return self.db.query(Message).filter(
            ((Message.sender_id == user_id) & (Message.receiver_id == contact_id)) |
            ((Message.sender_id == contact_id) & (Message.receiver_id == user_id))
        ).order_by(Message.timestamp).all()
        