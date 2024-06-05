import os
from dotenv import load_dotenv

load_dotenv()

SWAPI_BASE_URL = os.getenv("SWAPI_BASE_URL")
VISUAL_GUIDE_BASE_URL = os.getenv("VISUAL_GUIDE_BASE_URL")
placeholder_image = os.getenv("PLACEHOLDER_IMAGE")

character_image_urls = {
    "Luke Skywalker": f"{VISUAL_GUIDE_BASE_URL}1.jpg",
    "Darth Vader": f"{VISUAL_GUIDE_BASE_URL}4.jpg",
}
