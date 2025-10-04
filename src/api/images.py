import shutil

from fastapi import APIRouter, UploadFile

from src.services.images import ImageService
from src.tasks.tasks import resize_iamge


router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("/")
def add_image(file: UploadFile):
    ImageService().add_image(file)
  