from sqlalchemy import Column, Integer, Boolean, String, ForeignKey

from db.database import Base

class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True)
    is_group = Column(Boolean, nullable=False)
    chat_name = Column(String, nullable=True)
    last_message = Column(Integer, ForeignKey("messages.id")) 