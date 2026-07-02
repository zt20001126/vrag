from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


def save_upload_file(file: UploadFile, upload_dir: Path) -> str:
    upload_dir.mkdir(parents=True, exist_ok=True)

    original_name = Path(file.filename or "uploaded-image").name
    safe_name = f"{uuid4().hex}_{original_name}"
    target_path = upload_dir / safe_name

    with target_path.open("wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            buffer.write(chunk)

    return target_path.as_posix()
