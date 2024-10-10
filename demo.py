import gradio as gr
from banner_generator import BannerGenerator
from PIL import Image
import os
import configparser
from vertexai.preview.vision_models import GeneratedImage  # Import GeneratedImage

# Reading the configuration
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['credentials']['gemini_api_key']
proj_id = config['credentials']['gcp_project_id']

info = {"PROJECT_ID": proj_id, "LOCATION" : "us-central1", "API_KEY" : api_key}

# Function to generate the banner
def generate_banner(topic, images, aspect_ratio):
    # Initialize BannerGenerator with configs and the topic
    obj = BannerGenerator(CONFIGS=info, topic=topic)
    
    # Execute banner generation and obtain the image object
    banner_image = obj.execute(QC=False, passage=True)

    # Convert vertexai.preview.vision_models.GeneratedImage to a file path or PIL image
    temp_img_path = "/tmp/generated_banner.png"  # Define a temporary path to save the image
    
    # Ensure the generated image is of the correct type
    if isinstance(banner_image, GeneratedImage):
        # Access the image bytes directly and save it as a file
        banner_image.save(temp_img_path)

        # Open the saved image with PIL
        banner_image = Image.open(temp_img_path)

    return banner_image

# Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    # Main Container for UI elements
    with gr.Row():
        # Left Column: Introduction, Banner Topic, Aspect Ratio, Upload Images, and Generate Button
        with gr.Column(scale=1, min_width=300, elem_id="branding_section"):
            gr.Markdown(
                """
                <div style="text-align: left;">
                    <h1 style="font-size: 2.5rem; color: #ff6347; font-weight: bold;">Custom Banner Generator</h1>
                    <p style="font-size: 1.25rem; color: #333;">Create custom banners easily by entering your topic, selecting the aspect ratio, and uploading images.</p>
                </div>
                """, elem_id="intro_text"
            )
            # Input for banner details
            topic_input = gr.Textbox(label="📝 Banner Topic", placeholder="Enter banner topic (e.g., Product, Theme, etc.)", lines=2, elem_id="topic_input")
            
            # Dropdown for aspect ratio
            aspect_ratio_dropdown = gr.Dropdown(
                label="📐 Select Aspect Ratio",
                choices=["1:1", "9:16", "16:9", "4:3", "3:4"],
                elem_id="aspect_ratio_input"
            )
            
            # File upload for images
            image_input = gr.Files(label="📸 Upload Images", file_types=["image"], type="filepath", elem_id="image_input")
            
            # Button to generate the banner
            generate_button = gr.Button("✨ Generate Banner", size="large", elem_id="generate_button")

        # Right Column: Display the generated banner
        with gr.Column(scale=1, min_width=400, elem_id="interaction_section"):
            generated_image = gr.Image(label="🎨 Generated Banner", type="filepath", interactive=False, elem_id="generated_image")

            # Button to Trigger Banner Generation and Display the Generated Image
            generate_button.click(
                fn=generate_banner,
                inputs=[topic_input, image_input, aspect_ratio_dropdown],
                outputs=generated_image
            )

    # Footer
    gr.Markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <p style="font-size: 1.25rem; color: #888;">Powered by AI to simplify banner creation</p>
        </div>
        """, elem_id="footer_text"
    )

# Custom CSS for improving the UI layout
demo.css = """
    #branding_section {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 15px;
    }
    #interaction_section {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    #generate_button {
        width: 100%;
        margin-bottom: 15px;
        padding: 15px;
        font-size: 1.2rem;
        font-weight: bold;
        background-color: #ff6347;
        color: white;
        border: none;
        border-radius: 10px;
        cursor: pointer;
    }
    #generate_button:hover {
        background-color: #e5533d;
    }
    #generated_image {
        width: 100%;
        border: none;
        border-radius: 0px;
        object-fit: cover;
    }
"""

# Launch the demo
demo.launch(share=True)