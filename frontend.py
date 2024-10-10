import gradio as gr
import requests
import os

BASE_URL = "http://localhost:8000"

# Function to generate the banner
def generate_banner(topic, images, aspect_ratio):
    # Preparing files for the request
    files = [('images', (img.name, open(img.name, 'rb'))) for img in images]
    data = {
        'topic': topic,
        'aspect_ratio': aspect_ratio
    }
    response = requests.post(f"{BASE_URL}/generate_banner", data=data, files=files)
    
    # Close the files to prevent issues
    for _, (_, file) in files:
        file.close()
    
    if response.status_code == 200:
        result = response.json()
        image_path = result.get("image_path")
        if image_path:
            # Construct the full URL to access the generated image
            full_image_url = f"{BASE_URL}{image_path}"
            return full_image_url
        else:
            return "Error: Generated image not found."
    else:
        return "Error generating banner."

# Function to preview uploaded images
def preview_images(images):
    return images

# Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    # Main Container for UI elements
    with gr.Row():
        # Navigation Bar
        with gr.Column(scale=1, min_width=800):
            gr.Markdown(
                """
                <div style="background-color: #76B947; border-radius: 10px; padding: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);">
                    <h1 style="font-size: 2.5rem; color: white; text-align: center; margin: 0;">Bigbasket Banner Generator</h1>
                </div>
                """, elem_id="nav_bar"
            )
        
    with gr.Row():
        # Left Column: Introduction, Banner Topic, Aspect Ratio, Upload Images, and Generate Button
        with gr.Column(scale=1, min_width=300, elem_id="branding_section"):
            gr.Markdown(
                """
                <div style="text-align: left;">
                    <h2 style="font-size: 2rem; color: #ff6347; font-weight: bold;">Create Your Banner</h2>
                    <p style="font-size: 1.25rem; color: #444;">Create beautiful, impactful banners with ease! Simply upload images, enter the topic, and let our AI generate stunning banners for your projects.</p>
                    <p style="font-size: 1.1rem; color: #555;">Powered by <b>Google Gemini</b> and <b>Google Imagen</b>.</p>
                </div>
                """, elem_id="intro_text"
            )
            # Moved Banner Topic Input Below "Powered by" Text
            topic_input = gr.Textbox(label="📝 Banner Details (Product, Theme, Color, etc.)", placeholder="Enter the details for your banner", lines=2, elem_id="topic_input")
            aspect_ratio_dropdown = gr.Dropdown(
                label="📐 Select Aspect Ratio",
                choices=["1:1", "9:16", "16:9", "4:3", "3:4"],
                elem_id="aspect_ratio_input"
            )
            image_input = gr.Files(label="📸 Upload Images", file_types=["image"], type="filepath", elem_id="image_input")
            generate_button = gr.Button("✨ Generate Banner", size="large", elem_id="generate_button")

        # Right Column: Image Preview and Generated Banner
        with gr.Column(scale=1, min_width=400, elem_id="interaction_section"):
            image_preview = gr.Gallery(label="👀 Image Preview", elem_id="image_preview", show_label=False, height=300, preview=True)
            generated_image = gr.Image(label="🎨 Generated Banner", type="filepath", interactive=False, elem_id="generated_image")

            # Show uploaded images in the preview
            image_input.change(
                fn=preview_images,
                inputs=image_input,
                outputs=image_preview
            )

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
            <p style="font-size: 1.25rem; color: #888;">Made with ❤️ for creative designers</p>
            <p style="font-size: 1rem; color: #888;">Powered by Google Gemini and Google Imagen</p>
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
    #generated_image, #image_preview {
        width: 100%;
        border: none;
        border-radius: 0px;
        object-fit: cover;
    }
"""

# Launch the demo
demo.launch(share=True)

