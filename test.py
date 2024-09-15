import configparser
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel


config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['credentials']['gemini_api_key']
genai.configure(api_key = api_key)

item_selling = 'britannia marie biscuit'

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(f"""I'm selling {item_selling} online, and I need to generate an image of it.
  I need the image to be compelling and interesting to convince people to buy.
  Can you create a prompt I can use to generate an image of {item_selling} with Vertex?
  Respond with only the prompt, no other text. Be as verbose as possible.
  """)

prompt_image_gen = response.text


project_id = config['credentials']['gcp_project_id']
output_file = "images/sample/output_sample/my-output.png"
prompt = prompt_image_gen 

vertexai.init(project=project_id)

model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

images = model.generate_images(
    prompt=prompt,
    number_of_images=1,
    language="en",
    aspect_ratio="1:1",
    safety_filter_level="block_all"
)

images[0].save(location=output_file, include_generation_parameters=False)

print(f"Created output image using {len(images[0]._image_bytes)} bytes")