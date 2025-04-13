from ..repositories.message_repository import MessageRepository
from ..schemas.message import MessageCreate

class MessageService:
    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

    def send_message(self, sender_id: int, message: MessageCreate):
        return self.message_repo.create_message(sender_id, message)

    def get_conversation(self, user_id: int, contact_id: int):
        return self.message_repo.get_messages(user_id, contact_id)