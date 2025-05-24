from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from ..storage.minio_client import minio_client
from urllib.parse import quote

def get_avatar_file(object_name: str, bucket: str = "avatars") -> StreamingResponse:
    try:
        response = minio_client.get_object(bucket, object_name)
        content = BytesIO(response.read())
        return StreamingResponse(content, media_type="image/*")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Avatar not found")

def get_attachment_file(object_name: str, bucket: str = "attachments") -> StreamingResponse:
    try:
        response = minio_client.get_object(bucket, object_name)
        content = BytesIO(response.read())
        filename_encoded = quote(object_name)
        content_disposition = f"attachment; filename*=UTF-8''{filename_encoded}"

        return StreamingResponse(
            content,
            media_type="application/octet-stream",
            headers={"Content-Disposition": content_disposition}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Attachment not found")