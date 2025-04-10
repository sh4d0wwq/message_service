import httpx

async def is_user_in_chat(user_id: int, chat_id: int) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://chat-service/chats/{chat_id}/has_user/{user_id}")
        return response.status_code == 200