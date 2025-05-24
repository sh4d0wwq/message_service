from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from ..models.chat_user import ChatUser
from ..models.chat import Chat
from typing import List

class ChatUserRepository():
    def __init__(self, db: Session):
        self.db = db

    def get_chat_user_relation(self, user_id: int, chat_id: int) -> ChatUser | None:
        return self.db.query(ChatUser).filter(ChatUser.user_id == user_id, ChatUser.chat_id == chat_id).first()
    
    def find_private_chat_between_users(self, user1_id: int, user2_id: int) -> Chat | None:
        if user1_id == user2_id:
            return None
        
        chat_ids_with_both_users = (
            self.db.query(ChatUser.chat_id)
            .filter(ChatUser.user_id.in_([user1_id, user2_id]))
            .group_by(ChatUser.chat_id)
            .having(func.count(ChatUser.chat_id) == 2)
            .subquery()
        )

        return self.db.query(Chat).filter(
            Chat.is_group == False,
            Chat.chat_id.in_(chat_ids_with_both_users)
        ).first()
    
    def add_user_to_chat(self, chat_id: int, user_id: int) -> None:
        chat_user = ChatUser(chat_id = chat_id, user_id = user_id)
        self.db.add(chat_user)
        self.db.commit()
        self.db.refresh(chat_user)

    def get_user_chats(self, user_id: int) -> List[Chat] | None:
        chat_ids = (
            self.db.query(ChatUser.chat_id).filter(ChatUser.user_id == user_id).subquery()
        )

        return (
            self.db.query(Chat)
            .filter(Chat.chat_id.in_(chat_ids))
            .options(joinedload(Chat.last_message_obj))
            .all()
        )
    
    def get_another_user(self, chat_id: int, user_id: int):
        return self.db.query(ChatUser).filter(ChatUser.chat_id == chat_id, ChatUser.user_id != user_id).first()
        