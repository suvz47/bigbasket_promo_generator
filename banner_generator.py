import os
import configparser
import PIL
from PIL import Image
from typing import Any, List
from pydantic import BaseModel, Field
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel, GeneratedImage
from vertexai.preview.vision_models import Image as VertexImage

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['credentials']['gemini_api_key']
proj_id = config['credentials']['gcp_project_id']
info = {"PROJECT_ID": proj_id, "LOCATION": "us-central1", "API_KEY": api_key}

# Create directories for temporary and output images if they do not exist
os.makedirs('images/temp', exist_ok=True)
os.makedirs('images/output', exist_ok=True)

class BannerGenerator(BaseModel):
    """Class responsible for generating banners using generative models."""

    CONFIGS: dict
    topic: str
    images: List[str] | None = Field(default=None)
    text_model: str = "gemini-1.5-flash"
    image_model: str = "imagen-3.0-generate-001"
    edit_model: str = "imagegeneration@006"
    pm: Any = None
    im: Any = None
    em: Any = None
    text_v0: str = None
    text_v1: str = None
    text_v2: str = None
    text_v3: str = None
    img_response_v1: Any = None
    img_response_v2: Any = None
    img_response_v3: Any = None
    launch_state: bool = False

    def __launch(self):
        """Launches the generative models and sets up environment."""
        if not self.launch_state:
            vertexai.init(project=self.CONFIGS['PROJECT_ID'], location=self.CONFIGS['LOCATION'])
            genai.configure(api_key=self.CONFIGS['API_KEY'])
            self.pm = genai.GenerativeModel(self.text_model)
            self.im = ImageGenerationModel.from_pretrained(self.image_model)
            self.em = ImageGenerationModel.from_pretrained(self.edit_model)
            self.launch_state = True
            print("Model Launch successful!")

    def load_images(self) -> List[PIL.Image.Image]:
        """Loads images from file paths provided in the `images` attribute."""
        self.__launch()
        loaded_images = []

        for image_path in self.images:
            img = PIL.Image.open(image_path)
            if img.mode == 'RGBA':
                img = img.convert('RGB')  # Convert to RGB if needed
            loaded_images.append(img)

        return loaded_images

    def extract_image_information(self) -> str:
        """Extracts information from images using the generative text model."""
        images = self.load_images()
        extraction_prompt = '''Examine the set of images to provide concise unique insights about content, color, banner size, and product (name, logo, tagline, size, and packaging) in less than 150 words.'''
        model_input = [extraction_prompt] + images
        response = self.pm.generate_content(model_input)
        print("Attached images examined!")
        return response.text

    def extract_information(self) -> None:
        """Extracts information from the given topic and images using a detailed analysis."""
        self.__launch()

        out_text = f"""Deep analyze text from retail advertising, marketing psychology, and thoroughly researched marketing studies perspective: {self.topic}
        Extract the following information:
        0. Product: Product name, brand and supplier, logo, tagline, size, packaging if available
        1. Objective: 1 word for primary goal of the banner. Example - Awareness, Engagement, Conversion, Branding
        2. Age: The target age group. Example - 'Below 18', '18-25', '25-40', '40-60', '60+'
        3. Gender: Gender preference if applicable. Example - MALE, FEMALE, NON BINARY, ALL
        4. Festival: Event or occasion it may be tied to. Example - Christmas, Diwali, Black Friday, Summer Sale, New Year, Generic
        5. Headline: Suggest a main text that captures attention. Example - Discover [product] for [festival], Shop now and save!, Limited time offer, Innovate your life with [product]
        6. Subheadline: Optional additional supporting information to clarify the offer. Example - Get 50% off until [date], Exclusive deal for festive season, Hurry offer ends soon
        7. CTA: Add a call to action. Example - Buy now, Shop the collection, Discover More, Sign up today
        8. Color Scheme: Use color palette based on audience, occasion, or product tone. Example - Red & Gold (Festive, Urgency), Blue & White (Trust, Calm), Green & Brown (Eco-friendly, Natural), Black & White (Elegant, Minimal)
        9. Typography: Use font styles that resonate with the target demographic. Example - Sans-serif (Modern, Youthful), Serif (Traditional, Trustworthy), Script (Elegant, Formal), Display fonts (Playful, Bold)
        10. Visual Layout: Use layout pattern to guide user attention. Example - F pattern (Text-heavy), Z pattern (Balanced visuals & text)
        11. Imagery: Use of product images and contextual photos. If provided reuse them else create own. Examples - Multiple product angles, Lifestyle imagery, Holiday-themed images, Close-up product features
        12. Branding: Ensure logo placement and brand consistency. Top-left for logo, Consistent brand colors, Brand slogan or tagline inclusion
        13. Emotional Appeal: Emotion that the banner evokes based on psychographics and event. Example - Nostalgia (Older audiences, festive), Excitement (Younger audiences, sales), Trust and reliability (Product-focused), Aspiration (Luxury goods)
        14. Adaptability: If asked only then ensure banner scales well on mobile and other devices else only website design sizes. Example - Mobile-first design, Large, clear CTA, Minimal text for mobile
        15. Psychographics: Tailor the banner’s design, tone, and visuals based on psychographic factors and set levels for suitable OCEAN traits applicable. Example - [High/Low Openness (Innovation, Creativity): Innovative, creative visuals], [High/Low Conscientiousness (Order, Reliability): Clean, organized layout], [High/Low Extraversion (Vibrancy, Sociability): Bold colors, active themes], [High/Low Agreeableness (Warmth, Trust): Soft tones, community appeal], [High/Low Neuroticism (Stability, Reassurance)]
        16. Region: Location if applicable. Example - USA, London, India, Generic
        17. Specifications: Aspect ratio: 1:7, Resolution: 1360px (width) x 800px (height) (preferable for good resolution)
        18. Ethnicity: Identify target population group that will resonate well with product
        19. Promotional offer: Suggest 1 best promotional offer. Example - MAX ₹99 OFF, UP TO 60% OFF, UNDER ₹999, MIN ₹10 OFF, MIN 20% OFF, STARTS @₹99, FLAT ₹100 OFF, FLAT 20% OFF, ₹499 STORE, BUY 2 GET 1 FREE
        20. Background color gradient: Dynamic color generation to match overall look and feel
        21. Background theme: Festival oriented or generic if no festival
        """
        self.text_v0 = self.pm.generate_content(out_text).text

        # Information consolidation
        out_text = f"Respond concisely and summarize in Python dictionary format only this: {self.text_v0}"
        if self.images:
            image_info = self.extract_image_information()
            out_text += ' Product insights: ' + image_info
            print(f"Product insights: {image_info}")

        self.text_v1 = self.pm.generate_content(out_text).text[9:-5]

        # Scrapper to ensure data integrity and consistency
        out_text = f"Respond concisely by scrapping all unavailable information in Python dictionary format only this: {self.text_v1}"
        self.text_v2 = self.pm.generate_content(out_text).text

        print("Information collection complete!")

    def create_text_prompt(self) -> None:
        """Creates a text prompt based on the extracted information."""
        out_text = f"""Task: Fill in the values in this json: {self.text_v2}
        Guidelines:
        1. It will be used to generate an ads banner.
        2. Ensure it has all details pair-wise meticulously captured.
        3. All unknown/missing/unprovided variables are replaced with the attributes of the most probable shopper for that product.
        4. Recheck and identify all ambiguity or any text that leads to uncertainty.
        5. Replace all uncertainty with targeted values that make the most sense for the given product.
        6. Quantify everything possible, like high, medium, and lows to percentage values based on marketing and psychometric research studies.
        7. All KPIs and qualitative measures are to be used subcontextually only. Remove any details about statistical testing or names of any performance KPIs.
        8. Avoid sentences and use only necessary keywords.
        9. Remove all redundant key-value pairs.
        """
        self.text_v3 = self.pm.generate_content(out_text).text
        print("Information processed!")

    def generate_image(self) -> str:
        """Generates an image based on the given prompt and saves it in images/temp/."""
        prompt = f"""Realistic, subcontextually implied qualitative attributes inspired, excellent image quality ad capturing every detail in json:{self.text_v3}"""
        self.img_response_v1 = self.im.generate_images(prompt=prompt)

        # Save the generated image to images/temp/
        temp_img_path = 'images/temp/temp.jpg'
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
        self.img_response_v1.images[0].save(temp_img_path)

        print("Image v1 generated!")
        return temp_img_path

    def identify_lags(self) -> str:
        """Identifies quality issues in the generated image and provides suggestions for improvement."""
        prompt = f"""Be direct. Quality check the banner out of 10 on:
        1. Ensure visibility of brand name and logo
        2. Ensure background reflecting brand color consistency
        3. Ensure background if too bland then should be reflecting one of the following: people, culture, geographical, lifestage, product theme
        4. Promotional offer clearly applied and visible
        5. Ensure ALL texts pass grammatical checks
        6. Excellent image quality
        7. Jump up the image resolution if blurred
        8. Background gradient and theme aligned with context
        9. Aspect ratio to 1:7
        10. Resolution to 1360px (width) x 800px (height)
        11. Product name clear
        12. Product picture clear
        13. Product size clear if available
        14. Product packaging clear if available
        15. Product tagline clear if available

        Precisely point out errors and corresponding actions to fix the image where score is below 8.
        Do not output anything about elements that need no change. Suggest only minute to below-average changes, not drastic ones.
        Use this as a benchmark: {self.text_v3}
        """
        temp_img_path = 'images/temp/temp.jpg'
        response = self.pm.generate_content([prompt, PIL.Image.open(temp_img_path)])
        print(f'Lags identified: {response.text}')
        return response.text

    def fix_image(self, retest: bool = False) -> str:
        """Attempts to fix the identified lags in the generated image and saves it."""
        prompt = f'Realistic, subcontextually implied qualitative attributes inspired, excellent image quality ad by: {self.identify_lags()}'
        temp_img_path = 'images/temp/temp.jpg'

        base_image = VertexImage.load_from_file(location=temp_img_path)
        self.img_response_v2 = self.em.edit_image(
            base_image=base_image,
            prompt=prompt,
            edit_mode="inpainting-insert",
            mask_mode="background"
        )
        self.img_response_v2.images[0].save(temp_img_path)
        print("Image v2 generated!")

        if retest:
            prompt = f'Realistic, subcontextually implied qualitative attributes inspired, excellent image quality ad edit by: {self.identify_lags()}'
            self.img_response_v3 = self.em.edit_image(
                base_image=VertexImage.load_from_file(location=temp_img_path),
                prompt=prompt,
                edit_mode="inpainting-insert",
                mask_mode="background"
            )
            self.img_response_v3.images[0].save(temp_img_path)
            print("Image v3 generated!")

        # Save final image to output directory with a name corresponding to the topic
        output_filename = ''.join(e for e in self.topic if e.isalnum() or e == ' ')
        output_filename = output_filename[:50].strip().replace(' ', '_') + ".jpg"
        output_img_path = os.path.join('images/output', output_filename)
        self.img_response_v2.images[0].save(output_img_path)
        print(f"Final image saved as: {output_img_path}")

        return output_img_path

    def execute(self, QC=False) -> str:
        """Executes the entire workflow to generate and refine the banner."""
        self.extract_information()
        self.create_text_prompt()
        self.generate_image()
        final_image_path = self.fix_image(retest=QC)
        return final_image_path