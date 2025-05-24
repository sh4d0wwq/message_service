from ..repositories.chat_user_repository import ChatUserRepository
from ..models.chat_user import ChatUser
from ..utils.internal_requests import get_nickname_and_avatar_by_id
from typing import List
from ..models.chat import Chat

class ChatUserService:
    def __init__(self, chat_user_repo: ChatUserRepository):
        self.chat_user_repo = chat_user_repo

    def is_user_in_chat(self, user_id: int, chat_id: int) -> ChatUser | None:
        return self.chat_user_repo.get_chat_user_relation(user_id, chat_id)
    
    def get_user_chats(self, user_id: int) -> List[Chat] | None:
        chats = self.chat_user_repo.get_user_chats(user_id)
        for chat in chats:
            if not chat.is_group:
                another_user = self.chat_user_repo.get_another_user(chat.chat_id, user_id)
                nickname, avatar_url = get_nickname_and_avatar_by_id(another_user.user_id)
                setattr(chat, "contact_name", nickname)
                setattr(chat, "avatar_url", avatar_url)

        return chats