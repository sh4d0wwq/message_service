from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db.database import Base

class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True)
    is_group = Column(Boolean, nullable=False)
    chat_name = Column(String, nullable=True)
    last_message = Column(Integer, ForeignKey("messages.id")) 

    last_message_obj = relationship("Message", foreign_keys=[last_message])