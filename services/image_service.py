import json
from typing import Dict
import os
from config.config import VISUAL_GUIDE_BASE_URL, placeholder_image, character_image_urls
from services.character_service import get_character_data
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    with open('character_images_cache.json', 'r') as f:
        cached_images = json.load(f)
except FileNotFoundError:
    cached_images = {}

def save_cached_images():
    with open('character_images_cache.json', 'w') as f:
        json.dump(cached_images, f)

async def fetch_character_image(name: str) -> str:
    if name in cached_images:
        return cached_images[name]
    
    if name in character_image_urls:
        return character_image_urls[name]
    
    character_data = await get_character_data(name)
    if character_data:
        character_id = character_data['url'].split('/')[-2]
        image_url = f"{VISUAL_GUIDE_BASE_URL}{character_id}.jpg"
        cached_images[name] = image_url
        save_cached_images()
        return image_url
    
    return placeholder_image
