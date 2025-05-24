from ..repositories.message_repository import MessageRepository
from ..schemas.base_models import MessageCreate
from ..utils.internal_requests import get_nickname_and_avatar_by_id
from ..models.message import Message
from typing import List

class MessageService:
    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

    def send_message(self, sender_id: int, message: MessageCreate) -> Message:
        return self.message_repo.create_message(sender_id, message)

    def get_conversation(self, chat_id: int, limit: int, offset: int) -> List[Message] | None:
        messages = self.message_repo.get_messages(chat_id, limit, offset)

        for message in messages:
            nickname, avatar_url = get_nickname_and_avatar_by_id(message.sender_id)
            setattr(message, "nickname", nickname)
            setattr(message, "avatar_url", avatar_url)
        
        return messages
