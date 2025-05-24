from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException

from ..config import Config

class JWTService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, Config.ACCESS_SECRET_KEY, algorithm=Config.ALGORITHM) 
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, Config.REFRESH_SECRET_KEY, algorithm=Config.ALGORITHM)
    
    @staticmethod
    def verify_token(token: str, secret_key):
        try:
            payload = jwt.decode(token, secret_key, algorithms=[Config.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise
        except jwt.InvalidTokenError as e:
            raise e
        except jwt.PyJWTError as e:
            print("JWT Error:", e)
            raise HTTPException(status_code=401, detail=f"Invalid token: {e}")