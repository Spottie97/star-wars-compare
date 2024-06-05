from typing import Dict
import requests
import os
from config.config import SWAPI_BASE_URL

async def get_character_data(name: str) -> Dict:
    response = requests.get(SWAPI_BASE_URL, params={'search': name})
    if response.status_code == 200:
        data = response.json()
        if data['count'] > 0:
            return data['results'][0]
    return None

async def compare_attributes(attr1, attr2):
    try:
        if float(attr1) > float(attr2):
            return "character1"
        elif float(attr1) < float(attr2):
            return "character2"
        else:
            return "tie"
    except ValueError:
        if attr1 > attr2:
            return "character1"
        elif attr1 < attr2:
            return "character2"
        else:
            return "tie"

async def compare_characters(char1: Dict, char2: Dict) -> Dict:
    comparison = {}
    character1_wins = 0
    character2_wins = 0
    attributes = ['height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender']
    for attr in attributes:
        char1_value = char1.get(attr, 'unknown')
        char2_value = char2.get(attr, 'unknown')
        winner = await compare_attributes(char1_value, char2_value)
        comparison[attr] = {
            'character1': char1_value,
            'character2': char2_value,
            'winner': winner
        }
        if winner == "character1":
            character1_wins += 1
        elif winner == "character2":
            character2_wins += 1
    
    overall_winner = "character1" if character1_wins > character2_wins else "character2" if character2_wins > character1_wins else "tie"
    return comparison, overall_winner
