from fastapi import APIRouter, HTTPException
from services.character_service import get_character_data, compare_characters
from services.image_service import fetch_character_image
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/compare")
async def compare(name1: str, name2: str):
    logger.info(f"Comparing characters: {name1} and {name2}")
    
    char1 = await get_character_data(name1)
    char2 = await get_character_data(name2)

    if not char1 or not char2:
        logger.error("One or both characters not found")
        raise HTTPException(status_code=404, detail="One or both characters not found")

    comparison_result, overall_winner = await compare_characters(char1, char2)
    image1 = await fetch_character_image(name1)
    image2 = await fetch_character_image(name2)
    return {
        'comparison': comparison_result,
        'images': {
            'character1': image1,
            'character2': image2
        },
        'overall_winner': overall_winner
    }
