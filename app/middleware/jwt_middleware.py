from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from jwt import ExpiredSignatureError, InvalidTokenError
from ..services.jwt_service import JWTService
from ..config import Config

EXCLUDED_PATHS = [
    "/docs",
    "/openapi.json",
    "/redoc"
]

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(excluded) for excluded in EXCLUDED_PATHS):
            return await call_next(request)

        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        user_id = None

        if access_token:
            try:
                payload = JWTService.verify_token(access_token, Config.ACCESS_SECRET_KEY)
                user_id = payload.get("sub")
            except ExpiredSignatureError:
                pass 
            except InvalidTokenError:
                return Response("Invalid access token", status_code=401)

        if not user_id and refresh_token:
            try:
                refresh_payload = JWTService.verify_token(refresh_token, Config.REFRESH_SECRET_KEY)
                user_id = refresh_payload.get("sub")

                new_access_token = JWTService.create_access_token({"sub": user_id})
                new_refresh_token = JWTService.create_refresh_token({"sub": user_id})

                request.state.user_id = user_id
                response = await call_next(request)

                response.set_cookie("access_token", new_access_token, httponly=True)
                response.set_cookie("refresh_token", new_refresh_token, httponly=True)
                return response

            except ExpiredSignatureError:
                response = Response("Refresh token expired", status_code=401)
                response.delete_cookie("access_token")
                response.delete_cookie("refresh_token")
                return response
            except InvalidTokenError:
                return Response("Invalid refresh token", status_code=401)

        if user_id:
            request.state.user_id = user_id
            return await call_next(request)

        return Response("Unauthorized", status_code=401)
