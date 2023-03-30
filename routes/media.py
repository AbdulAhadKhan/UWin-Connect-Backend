import io
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from utils.utils import get_file

media_router = APIRouter()


@media_router.get("/get-image/{image_name}", status_code=200,
                  responses={200: {"message": "Image retrieved successfully"},
                             404: {"message": "Image not found"}},
                  response_class=Response)
async def get_image(image_name: str):
    try:
        image = io.BytesIO(await get_file(image_name))
        headers = {
            "Content-Type": 'image/*',
            "Content-Disposition": "inline",
        }
        return Response(content=image.getvalue(), headers=headers)
    except Exception:
        raise HTTPException(status_code=404, detail="Image not found")
