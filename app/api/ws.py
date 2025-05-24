from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from ..dependencies import get_current_ws_user_id, get_message_service, get_db
from ..schemas.base_models import MessageCreate
from ..services.chat_user_service import ChatUserService
from ..services.message_service import MessageService
from ..repositories.chat_user_repository import ChatUserRepository
import json
from ..utils.internal_requests import get_nickname_and_avatar_by_id

class ChatWebSocketHandler:
    def __init__(self):
        self.router = APIRouter()
        self.active_connections: dict[int, list[WebSocket]] = {}
        self.router.add_api_websocket_route(
            "/ws/chat/{chat_id}",
            self.websocket_endpoint
        )

    def get_chat_user_service(self, db): 
        return ChatUserService(ChatUserRepository(db))

    async def websocket_endpoint(
        self,
        websocket: WebSocket,
        chat_id: int,
        message_service: MessageService = Depends(get_message_service),
        db = Depends(get_db)
    ):
        user_id = await get_current_ws_user_id(websocket)
        chat_user_service = self.get_chat_user_service(db)
        await self.connect(chat_id, websocket, user_id, message_service, chat_user_service)

    async def connect(self, chat_id: int, websocket: WebSocket, user_id, message_service: MessageService, chat_user_service: ChatUserService):
        await websocket.accept()

        if not chat_user_service.is_user_in_chat(user_id, chat_id):
            await websocket.close(code=1008)
            return

        self.active_connections.setdefault(chat_id, []).append(websocket)

        try:
            while True:
                data = await websocket.receive_text()
                json_data = json.loads(data)

                content = json_data.get("content", "")
                attachment_url = json_data.get("attachment_url")

                message_create = MessageCreate(
                    chat_id=chat_id,
                    content=content,
                    attachment_url=attachment_url
                )
                message = message_service.send_message(sender_id=user_id, message=message_create)
                username, avatar_url = get_nickname_and_avatar_by_id(user_id)
                response_data = {
                    "type": "message",
                    "chat_id": chat_id,
                    "sender_id": user_id,
                    "content": message.content,
                    "attachment_url": message.attachment_url,
                    "sender_name": username,
                    "avatar_url": avatar_url,
                    "timestamp": message.timestamp.isoformat()
                }

                for conn in self.active_connections[chat_id]:
                    await conn.send_text(json.dumps(response_data))

        except WebSocketDisconnect:
            self.active_connections[chat_id].remove(websocket)


chat_ws_handler = ChatWebSocketHandler()
router = chat_ws_handler.router    