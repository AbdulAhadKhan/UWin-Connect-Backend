import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

media_router = APIRouter()


@media_router.get("/get-image/{image}", status_code=200,
                  responses={200: {"message": "Image retrieved successfully"},
                             404: {"message": "Image not found"}},
                  response_class=FileResponse)
async def get_image(image: str):
    file = f".data/{image}"
    if os.path.exists(file):
        return FileResponse(file)
    raise HTTPException(status_code=404, detail="Image not found")
