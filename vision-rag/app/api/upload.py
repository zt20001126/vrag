from fastapi import APIRouter, File, UploadFile

from app.services.image_service import image_service


router = APIRouter()


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)) -> dict[str, str]:
    saved_path = image_service.save_uploaded_image(file)
    return {
        "message": "upload success",
        "filename": file.filename or "",
        "file_path": saved_path,
    }
