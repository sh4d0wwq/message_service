from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from jwt import ExpiredSignatureError, InvalidTokenError
from ..services.jwt_service import JWTService

EXCLUDED_PATHS = [
    "/auth/login",
    "/auth/register",
]

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
            return await call_next(request)
        
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")
        if access_token:
            try:
                payload = JWTService.verify_token(access_token) 
                request.state.user_id = payload["sub"]
                return await call_next(request)
            except ExpiredSignatureError:
                if refresh_token:  
                    try:
                        user_data = JWTService.verify_token(refresh_token)
                        new_access_token = JWTService.create_access_token({"sub": user_data["sub"]})
                        
                        response = await call_next(request)
                        response.set_cookie(key="access_token", value=new_access_token, httponly=True)
                        return response
                    except ExpiredSignatureError:
                        response = Response("Refresh token expired", status_code=401)
                        response.delete_cookie("access_token")
                        response.delete_cookie("refresh_token")
                        return response
                else:
                    return Response("Unauthorized", status_code=401)
            except InvalidTokenError:
                return Response("Invalid token", status_code=401)
        
        return Response("Unauthorized", status_code=401)