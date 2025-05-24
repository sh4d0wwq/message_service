from pydantic import BaseModel
from typing import Optional, List

class MessageCreate(BaseModel):
    chat_id: int
    content: str
    attachment_url: Optional[str] = None

class CreateGroupChatRequest(BaseModel):
    chat_name: str
    user_ids: List[int]

class AddUserRequest(BaseModel):
    chat_id: int
    user_id: int

class ChatResponse(BaseModel):
    chat_id: int

class MessageModel(BaseModel):
    id: int
    sender_id: int
    content: str
    attachment_url: Optional[str] = None
    nickname: str
    avatar_url: Optional[str] = None

class MessageResponse(BaseModel):
    messages: List[MessageModel]

class ChatOut(BaseModel):
    chat_id: int
    is_group: bool
    chat_name: Optional[str] = None
    last_message: Optional[int] = None
    contact_name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        orm_mode = True