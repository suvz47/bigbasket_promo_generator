import configparser
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import random 


config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['credentials']['gemini_api_key']
genai.configure(api_key = api_key)

product = 'pepsi and coca cola'
promo = '20 percent discount'
color = 'red, white, green, orange and blue'
theme = 'durga puja'
aspect_ratio = '1:1'
format = 'banner'


model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(f"""I'm selling {product} online on the occasion of {theme}, and I need to generate an image of it. 
                                  There is a promotional of {promo}. The color pallete should be {color}. 
                                  I need the image to be compelling and interesting to convince people to buy for the occassion of {theme}.
                                  Can you create a prompt I can use to generate an image of {product} with Vertex? Be very accurate about 
                                  the product description, don't make up random stuff. Respond with only the prompt, no other text. 
                                  Be as verbose as possible, and something out of the box for the occassion of {theme}. 
                                  Add instrunctions to make sure than any text in the image is spelt correctly and only in English, 
                                  and properly aligned.
  """)

prompt_image_gen = response.text + 'Make sure the text is spelt correctly, only with english letters, and aligned properly.'
print(prompt_image_gen)


project_id = config['credentials']['gcp_project_id']
random_num = random.randrange(100, 100000, 3)
output_file = f"images/sample/output_sample/{product}_{theme}_{color}_{promo}_{random_num}.png"
prompt = prompt_image_gen 

vertexai.init(project=project_id)

model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

images = model.generate_images(
    prompt=prompt,
    number_of_images=1,
    language="en",
    aspect_ratio=aspect_ratio,
    safety_filter_level="block_all"
)

images[0].save(location=output_file, include_generation_parameters=False)

print(f"Created output image using {len(images[0]._image_bytes)} bytes")