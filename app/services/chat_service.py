from ..repositories.chat_repository import ChatRepository
from ..repositories.chat_user_repository import ChatUserRepository
from typing import List
from ..models.chat import Chat

class ChatService:
    def __init__(self, chat_repo: ChatRepository, chat_user_repo: ChatUserRepository):
        self.chat_repo = chat_repo
        self.chat_user_repo = chat_user_repo

    def get_private_chat(self, user_id: int, sender_id: int) -> Chat | None:
        chat = self.chat_user_repo.find_private_chat_between_users(user_id, sender_id)
        if chat:
            return chat
        
        chat = self.chat_repo.create_chat(False)
        self.chat_user_repo.add_user_to_chat(chat.chat_id, user_id)
        self.chat_user_repo.add_user_to_chat(chat.chat_id, sender_id)
        
        return chat
    
    def create_group_chat(self, user_ids: List[int], chat_name: str) -> Chat | None:
        chat = self.chat_repo.create_chat(is_group=True, chat_name=chat_name)

        for user_id in user_ids:
            self.chat_user_repo.add_user_to_chat(chat.chat_id, user_id)

        return chat