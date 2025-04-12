from sqlalchemy import Column, Integer, ForeignKey

from db.database import Base

class ChatUser(Base):
    __tablename__ = "chat_user"

    chat_id = Column(Integer, ForeignKey("chats.chat_id"), primary_key=True)
    user_id = Column(Integer, primary_key=True)