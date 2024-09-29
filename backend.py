from fastapi import FastAPI, UploadFile, Form
from typing import List
from banner_generator import BannerGenerator, info
import io
from PIL import Image
import os

app = FastAPI()

@app.post("/generate_banner")
async def generate_banner(
    topic: str = Form(...),
    images: List[UploadFile] = None
):
    # Create the BannerGenerator instance with fixed configuration info from `info`
    banner_generator = BannerGenerator(CONFIGS=info, topic=topic)

    # Create the directory if it does not exist
    tmp_dir = "/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    # Save uploaded images
    image_paths = []
    for image in images:
        content = await image.read()
        img = Image.open(io.BytesIO(content))
        
        # Convert image to RGB if it's in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        img_path = os.path.join(tmp_dir, image.filename)
        img.save(img_path)
        image_paths.append(img_path)

    # Set images for banner generation
    banner_generator.images = image_paths

    # Generate banner
    image_path = banner_generator.execute()

    return {"message": "Banner generated successfully", "image_path": image_path}