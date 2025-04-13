from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from ..dependencies import get_current_user_id, get_message_service, get_db
from ..schemas.message import MessageCreate
from ..services.chat_user_service import ChatUserService
from ..services.message_service import MessageService
from ..repositories.chat_user_repository import ChatUserRepository
import json

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
        user_id: int = Depends(get_current_user_id),
        message_service: MessageService = Depends(get_message_service),
        db = Depends(get_db)
    ):
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

                message_create = MessageCreate(chat_id=chat_id, content=json_data["content"])
                message = message_service.send_message(sender_id=user_id, message=message_create)

                response_data = {
                    "type": "message",
                    "chat_id": chat_id,
                    "sender_id": user_id,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat()
                }

                for conn in self.active_connections[chat_id]:
                    await conn.send_text(json.dumps(response_data))

        except WebSocketDisconnect:
            self.active_connections[chat_id].remove(websocket)
