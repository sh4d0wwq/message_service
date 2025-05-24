import uuid
from fastapi import UploadFile
from ..storage.minio_client import minio_client
import io

async def upload_file_to_minio(file: UploadFile, bucket: str) -> str:
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_data = await file.read()

    minio_client.put_object(
        bucket_name=bucket,
        object_name=filename,
        data=io.BytesIO(file_data),
        length=len(file_data),
        content_type=file.content_type
    )

    return filename
