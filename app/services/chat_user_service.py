from ..repositories.chat_user_repository import ChatUserRepository
from ..models.chat_user import ChatUser

class ChatUserService:
    def __init__(self, chat_user_repo: ChatUserRepository):
        self.chat_user_repo = chat_user_repo

    def is_user_in_chat(self, user_id: int, chat_id: int) -> ChatUser | None:
        return self.chat_user_repo.get_chat_user_relation(user_id, chat_id)