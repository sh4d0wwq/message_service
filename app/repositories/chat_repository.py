from sqlalchemy.orm import Session
from ..models.chat import Chat

class ChatRepository():
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, is_group: bool = False):
        chat = Chat(is_group = is_group)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat
