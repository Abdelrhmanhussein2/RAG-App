from fastapi import APIRouter, UploadFile, Depends, Request
from controllers import DataController, ProjectController,processController
from helpers.config import settings
from fastapi.responses import JSONResponse
import aiofiles
import os
from routes.schemes import process
from models.enums.ResponseEnums import ResponseStatus
from models import BaseDataModel,ProjectModel
from models.db_schemes import DataChunk
from models.ChunkModel import ChunkModel

data_router = APIRouter(prefix="/data", tags=["Data"])


@data_router.post("/upload/{project_id}")
async def upload_file(request: Request, project_id: str, file: UploadFile,
                    app_settings = Depends(lambda: settings)):
    project_model = await ProjectModel.create_instance(db_client=request.app.mongodb)
    project=await project_model.get_project_or_create(project_id=project_id)
    
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
        print(f"Error saving file: {e}")
        return {"message": ResponseStatus.UPLOAD_FAILED.value}

    return JSONResponse(
    content={
        "message": ResponseStatus.FILE_VALIDATED_SUCCESS.value,
        "file_id": file_id,
        "project_id": str(project.project_id)
        
    },
    status_code=200
)
    
    
    
    
@data_router.post("/process/{project_id}")
async def process_file(request: Request, project_id: str, process_request: process):
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap=process_request.overlap
    do_reset=process_request.do_reset
    project_model = await ProjectModel.create_instance(db_client=request.app.mongodb)
    project= await project_model.get_project_or_create(project_id=project_id)
    
    chunk_model = await ChunkModel.create_instance(db_client=request.app.mongodb)
    deleted_count = 0
    if do_reset:
        deleted_count = await chunk_model.delete_project_chunks(project_id=project_id)
        print(f"Entities deleted: {deleted_count}")

    file_content=processController(project_id=project_id).get_content(file_id=file_id)
    file_chunks=processController(project_id=project_id).split_content(
        content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    
    if file_chunks is None:
        return JSONResponse(
            content={
                "message": ResponseStatus.PROCESSING_FAILED.value
            },
            status_code=500
        )

    file_chunk_record=[
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_order=i,
            chunk_project_id=project_id,
        )
        for i, chunk in enumerate(file_chunks)
    ]

    records=await chunk_model.insert_many_chunk(chunk=file_chunk_record)

    return JSONResponse(
        content={
            "message": ResponseStatus.PROCESSING_SUCCESS.value,
            "records": records,
            "deleted_count": deleted_count
        },
        status_code=200
    )
