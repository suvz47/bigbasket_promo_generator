import gradio as gr
import requests

BASE_URL = "http://localhost:8000"

# Function to generate the banner
def generate_banner(topic, images):
    files = [('images', (img.name, open(img, 'rb'))) for img in images]
    data = {
        'topic': topic,
    }
    response = requests.post(f"{BASE_URL}/generate_banner", data=data, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("image_path")
    else:
        return "Error generating banner."

# Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:  # Using a modern theme
    gr.Markdown(
        """
        <div style="text-align: center;">
            <h1 style="font-size: 3rem; color: #ff6347; font-weight: bold;">🎨 Banner Generator for Designers 🎨</h1>
            <p style="font-size: 1.25rem; color: #333;">Create beautiful, impactful banners with ease! Simply upload images, enter the topic, and let our AI generate stunning banners for your projects.</p>
        </div>
        """
    )

    topic_input = gr.Textbox(label="📝 Banner Topic", placeholder="Enter the topic for your banner")
    image_input = gr.Files(label="📸 Upload Images", file_types=["image"], type="filepath")  # Allow uploading of multiple images
    generate_button = gr.Button("✨ Generate Banner")
    generated_image = gr.Image(label="🎨 Generated Banner", type="filepath", interactive=False)

    generate_button.click(
        generate_banner,
        inputs=[topic_input, image_input],
        outputs=generated_image
    )

    gr.Markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <p style="font-size: 1.25rem; color: #888;">Made with ❤️ for creative designers</p>
        </div>
        """
    )

demo.launch(share=True)