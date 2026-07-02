from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from requests import RequestException
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import init_db
from app.services.embedding_service import embedding_service
from app.services.image_service import image_service
from app.vector.client import pgvector_client


router = APIRouter()


@router.post("/upload")
async def upload_image(
    designer_id: int = Form(...),
    file: UploadFile = File(...),
) -> dict[str, object]:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are supported.")

    try:
        init_db()
        saved_path = image_service.save_uploaded_image(file)
        embedding = embedding_service.embed_image_file(saved_path)
        image_url = f"/uploads/{Path(saved_path).name}"
        record = pgvector_client.create_image(
            image_url=image_url,
            designer_id=designer_id,
            embedding=embedding,
        )
    except (RequestException, RuntimeError, SQLAlchemyError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "message": "upload success",
        "image_id": record["id"],
        "filename": file.filename or "",
        "file_path": saved_path,
        "image_url": image_url,
        "designer_id": designer_id,
        "embedding_dimension": len(embedding),
    }
