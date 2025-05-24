from fastapi import APIRouter, Depends, Query, UploadFile, File
from typing import List
from ..dependencies import get_current_user_id, get_message_service, get_chat_service, get_chat_user_service
from ..services.message_service import MessageService
from ..services.chat_service import ChatService
from ..services.chat_user_service import ChatUserService
from ..utils.upload_file import upload_file_to_minio
from ..utils.download_file import get_attachment_file
from ..schemas.base_models import CreateGroupChatRequest, AddUserRequest, MessageResponse, ChatResponse, ChatOut

class MessageAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/chats", tags=["Chats"])
        self.router.add_api_route(
            "/msg/{chat_id}", 
            self.get_conversation, 
            methods=["GET"],
            response_model=MessageResponse,
            summary="Получить переписку чата",
            description="Возвращает список сообщений в чате с поддержкой пагинации (limit и offset)."
        )

        self.router.add_api_route(
            "/p/{user_id}", 
            self.get_private_chat, 
            methods=["GET"],
            response_model=ChatResponse,
            summary="Получить приватный чат",
            description="Создает или возвращает ID приватного чата между текущим пользователем и указанным user_id."
        )

        self.router.add_api_route(
            "/updates", 
            self.get_user_chats, 
            methods=["GET"],
            response_model=List[ChatOut],
            summary="Получить список чатов пользователя",
            description="Возвращает все чаты, в которых участвует текущий пользователь."
        )

        self.router.add_api_route(
            "/upload", 
            self.upload_file, 
            methods=["POST"],
            summary="Загрузить файл",
            description="Загружает файл (например, вложение в чат) в MinIO и возвращает его URL."
        )

        self.router.add_api_route(
            "/download/{file_url}", 
            self.download_file, 
            methods=["GET"],
            summary="Скачать файл",
            description="Возвращает файл по указанному URL из MinIO."
        )

        self.router.add_api_route(
            "/group", 
            self.create_group_chat, 
            methods=["POST"],
            response_model=ChatResponse,
            summary="Создать групповой чат",
            description="Создает новый групповой чат с заданными участниками и названием."
        )

        self.router.add_api_route(
            "/add-user", 
            self.add_chat_member, 
            methods=["PATCH"],
            summary="Добавить пользователя в чат",
            description="Добавляет пользователя в указанный групповой чат."
        )

    def get_private_chat(
            self, 
            user_id: int, 
            chat_service: ChatService = Depends(get_chat_service), 
            sender_id: int = Depends(get_current_user_id)
    ):
        """Создает/возвращает приватный чат между двумя пользователями."""
        if sender_id == user_id:
            return {"response": "Error"}
        chat = chat_service.get_private_chat(user_id, sender_id)
        return {"chat_id": chat.chat_id}
    
    def create_group_chat(
            self, 
            request: CreateGroupChatRequest, 
            chat_service: ChatService = Depends(get_chat_service), 
            cur_user_id: int = Depends(get_current_user_id)
    ):
        """Создает групповой чат с заданными пользователями и названием."""
        user_ids = request.user_ids
        user_ids.append(cur_user_id)
        return chat_service.create_group_chat(user_ids, request.chat_name)

    def get_conversation(
            self, 
            chat_id: int, 
            message_service: MessageService = Depends(get_message_service), 
            limit: int = Query(20), 
            offset: int = Query(0)
    ):
        """Возвращает сообщения из чата."""
        return {"messages": message_service.get_conversation(chat_id, limit, offset)}

    def get_user_chats(
            self, 
            user_id: int = Depends(get_current_user_id), 
            chat_user_service: ChatUserService = Depends(get_chat_user_service)
    ):
        """Получить все чаты текущего пользователя."""
        return chat_user_service.get_user_chats(user_id)
    
    async def upload_file(
            self, 
            file: UploadFile = File(...)
    ):
        """Загрузить файл в MinIO и вернуть URL."""
        filename = await upload_file_to_minio(file, bucket="attachments")
        return {"url": filename}
    
    async def download_file(
            self, 
            file_url
    ):
        """Скачать файл из MinIO по URL."""
        return get_attachment_file(file_url)
    
    def add_chat_member(
            self, 
            request: AddUserRequest, 
            chat_user_service: ChatUserService = Depends(get_chat_user_service)
    ):
        """Добавить пользователя в указанный чат."""
        return chat_user_service.chat_user_repo.add_user_to_chat(request.chat_id, request.user_id)
    

message_api = MessageAPI()
router = message_api.router    