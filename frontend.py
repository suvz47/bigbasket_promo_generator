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
    # Main Container for UI elements
    with gr.Row():
        # Left Column: Logos and Introduction
        with gr.Column(scale=1, min_width=300, elem_id="branding_section"):
            # Logos for Bigbasket, Google, and Gemini - Without borders, buttons, or shadows
            with gr.Row():
                gr.Image(value="images/logos/bigbasket_logo.png", show_label=False, interactive=False, elem_id="logo_bigbasket")
                gr.Image(value="images/logos/google_logo.png", show_label=False, interactive=False, elem_id="logo_google")
                gr.Image(value="images/logos/gemini_logo.png", show_label=False, interactive=False, elem_id="logo_gemini")

            gr.Markdown(
                """
                <div style="text-align: left;">
                    <h1 style="font-size: 2.5rem; color: #ff6347; font-weight: bold;">Bigbasket Banner Generator</h1>
                    <p style="font-size: 1.25rem; color: #333;">Create beautiful, impactful banners with ease! Simply upload images, enter the topic, and let our AI generate stunning banners for your projects.</p>
                    <p style="font-size: 1.1rem; color: #555;">Powered by <b>Google Gemini</b> and <b>Google Imagen</b>.</p>
                </div>
                """, elem_id="intro_text"
            )

        # Right Column: Inputs and Output
        with gr.Column(scale=1, min_width=400, elem_id="interaction_section"):
            with gr.Row():
                topic_input = gr.Textbox(label="📝 Banner Topic", placeholder="Enter the details for your banner", lines=7, elem_id="topic_input")  # Increased height to 3 lines
                image_input = gr.Files(label="📸 Upload Images", file_types=["image"], type="filepath", elem_id="image_input")  # Allow uploading of multiple images

            generate_button = gr.Button("✨ Generate Banner", size="large", elem_id="generate_button")
            generated_image = gr.Image(label="🎨 Generated Banner", type="filepath", interactive=False, elem_id="generated_image")

            generate_button.click(
                generate_banner,
                inputs=[topic_input, image_input],
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

# Custom CSS for improving the UI layout and matching logo background
demo.css = """
    #branding_section {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 15px;
    }
    #logo_bigbasket, #logo_google, #logo_gemini {
        width: 80px;
        height: 80px;
        margin: 0 10px;
        background: none;  /* Ensure there is no background on logos */
        border: none;  /* Remove border to blend with the page */
    }
    #intro_text {
        padding-top: 15px;
    }
    #interaction_section {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    #topic_input {
        margin-bottom: 10px;
        height: auto;  /* Let the height adjust to accommodate the number of lines */
    }
    #image_input {
        margin-bottom: 10px;
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
        border: none;  /* Remove border around the generated image */
        border-radius: 0px;
    }
    #footer_text {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 15px;
    }
"""

# Launch the demo with side-by-side layout and modern branding
demo.launch(share=True)