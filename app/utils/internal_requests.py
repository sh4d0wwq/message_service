import httpx

headers = {"X-Internal-Secret": "WowItsSoSecret"}

def get_nickname_and_avatar_by_id(user_id: int) -> str | None:
        try:
            response = httpx.get(f"http://user_service:8000/users/internal/{user_id}", headers=headers)
            response.raise_for_status()
            return response.json().get("nickname"), response.json().get("avatar_url")
        except httpx.HTTPError:
            return None