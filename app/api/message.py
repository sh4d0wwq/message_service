from fastapi import APIRouter, Depends
from ..dependencies import get_current_user_id, get_message_service, get_chat_service
from ..services.message_service import MessageService
from ..services.chat_service import ChatService

class MessageAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/msg", tags=["Messages"])
        self.router.add_api_route("/{contact_id}", self.get_conversation, methods=["GET"])
        self.router.add_api_route("/p/{user_id}", self.get_private_chat, methods=["POST"])

    def get_private_chat(self, user_id: int, chat_service: ChatService = Depends(get_chat_service), sender_id: int = Depends(get_current_user_id)):
        chat = chat_service.get_private_chat(user_id, sender_id)
        return {"chat_id": chat.chat_id}

    def get_conversation(self, contact_id: int, user_id: int = Depends(get_current_user_id), message_service: MessageService = Depends(get_message_service)):
        return message_service.get_conversation(user_id, contact_id)

message_api = MessageAPI()
router = message_api.router    