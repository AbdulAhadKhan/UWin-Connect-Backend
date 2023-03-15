from fastapi import APIRouter
from fastapi.responses import FileResponse

media_router = APIRouter()

@media_router.get("/get-image/{image}", status_code=200, 
                  responses={200: {"message": "Image retrieved successfully"}},
                  response_class=FileResponse)
async def get_image(image: str):
    return f".data/{image}"