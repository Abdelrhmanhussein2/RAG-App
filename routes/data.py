from fastapi import APIRouter, UploadFile, Depends
from controllers import DataController, ProjectController
from helpers.config import get_settings, setting
from fastapi.responses import JSONResponse
import aiofiles
import os

data_router = APIRouter(prefix="/data", tags=["Data"])

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile,
                    app_settings: setting = Depends(get_settings)):

    is_valid, result_signal = DataController().validate_file(file=file)

    if not is_valid:
        return {
            "is_valid": is_valid,
            "result_signal": result_signal
        }

    project_dir_path = ProjectController().get_projects(project_id=project_id)

    os.makedirs(project_dir_path, exist_ok=True)

    file_path, file_id = DataController().generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
        print(f"Error occurred while uploading file: {e}")
        return {"message": "Upload failed"}

    return JSONResponse(
        content={"message": "File uploaded successfully"},
        status_code=200
    )