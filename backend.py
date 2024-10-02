from fastapi import FastAPI, UploadFile, Form
from typing import List, Optional
from banner_generator import BannerGenerator, info  # Import BannerGenerator and info
import shutil
import os
from fastapi.responses import FileResponse

app = FastAPI()

# Ensure directories for saving images exist
os.makedirs('images/temp', exist_ok=True)
os.makedirs('images/output', exist_ok=True)

# Endpoint for generating a banner
@app.post("/generate_banner")
async def generate_banner(
    topic: str = Form(...),
    images: List[UploadFile] = Form(...),
    aspect_ratio: Optional[str] = Form(None)  # Added aspect_ratio as input parameter
):
    # Save uploaded images to disk
    image_paths = []
    for image in images:
        temp_path = f"images/temp/{os.path.basename(image.filename)}"
        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_paths.append(temp_path)
        except FileNotFoundError as e:
            return {"error": f"Could not save image: {e}"}

    # Create a BannerGenerator instance
    banner_generator = BannerGenerator(
        CONFIGS=info,
        topic=topic,
        images=image_paths,
        aspect_ratio=aspect_ratio  # Pass the aspect_ratio parameter
    )

    # Execute the banner generation process
    try:
        final_image_path = banner_generator.execute()
    except Exception as e:
        return {"error": f"Banner generation failed: {e}"}

    # Return the relative path to the generated banner image
    return {"image_path": f"/images/{os.path.basename(final_image_path)}"}

# Endpoint to serve images
@app.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join("images/output", image_name)
    if not os.path.exists(image_path):
        return {"error": "Image not found"}
    return FileResponse(image_path)