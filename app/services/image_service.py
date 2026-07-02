from fastapi import UploadFile

from app.core.config import settings
from app.utils.file_utils import save_upload_file


class ImageService:
    def save_uploaded_image(self, file: UploadFile) -> str:
        return save_upload_file(file=file, upload_dir=settings.UPLOAD_DIR)


image_service = ImageService()
