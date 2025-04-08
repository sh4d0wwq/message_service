from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependenices import get_db, get_current_user_id
from ..models.message import MessageCreate
from ..services.message_service import MessageService
from ..repositories.message_repository import MessageRepository

class UserAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/messages", tags=["Messages"])
        self.router.add_api_route("/", self.send_message, methods=["POST"])
        self.router.add_api_route("/{contact_id}", self.get_conversation, methods=["GET"])

    def get_message_service(self, db: Session) -> MessageService:
        return MessageService(MessageRepository(db))

    def send_message(self, message: MessageCreate, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
        message_service = self.get_message_service(db)
        return message_service.send_message(user_id, message)

    def get_conversation(self, contact_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
        message_service = self.get_message_service(db)
        return message_service.get_conversation(user_id, contact_id)

user_api = UserAPI()
router = user_api.router    