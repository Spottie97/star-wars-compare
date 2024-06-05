import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, get_character_data, fetch_character_image, compare_characters

client = TestClient(app)

# Mock data for characters
character_data_luke = {
    "name": "Luke Skywalker",
    "height": "172",
    "mass": "77",
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color": "blue",
    "birth_year": "19BBY",
    "gender": "male",
    "url": "https://swapi.dev/api/people/1/"
}

character_data_vader = {
    "name": "Darth Vader",
    "height": "202",
    "mass": "136",
    "hair_color": "none",
    "skin_color": "white",
    "eye_color": "yellow",
    "birth_year": "41.9BBY",
    "gender": "male",
    "url": "https://swapi.dev/api/people/4/"
}

@pytest.fixture
def mock_get_character_data():
    with patch('main.get_character_data') as mock:
        yield mock

@pytest.fixture
def mock_fetch_character_image():
    with patch('main.fetch_character_image') as mock:
        yield mock

def test_compare_characters_success(mock_get_character_data, mock_fetch_character_image):
    mock_get_character_data.side_effect = [character_data_luke, character_data_vader]
    mock_fetch_character_image.side_effect = [
        "https://starwars-visualguide.com/assets/img/characters/1.jpg",
        "https://starwars-visualguide.com/assets/img/characters/4.jpg"
    ]

    response = client.get("/compare", params={"name1": "Luke Skywalker", "name2": "Darth Vader"})
    assert response.status_code == 200

    data = response.json()
    assert "comparison" in data
    assert "images" in data
    assert "overall_winner" in data
    assert data["images"]["character1"] == "https://starwars-visualguide.com/assets/img/characters/1.jpg"
    assert data["images"]["character2"] == "https://starwars-visualguide.com/assets/img/characters/4.jpg"
    assert data["overall_winner"] in ["character1", "character2", "tie"]

def test_compare_characters_not_found(mock_get_character_data):
    mock_get_character_data.side_effect = [None, character_data_vader]

    response = client.get("/compare", params={"name1": "Unknown Character", "name2": "Darth Vader"})
    assert response.status_code == 404
    assert response.json() == {"detail": "One or both characters not found"}

def test_compare_attributes():
    result = compare_characters(character_data_luke, character_data_vader)
    comparison, overall_winner = result
    assert overall_winner in ["character1", "character2", "tie"]
    assert "height" in comparison
    assert "mass" in comparison
    assert "hair_color" in comparison
    assert "skin_color" in comparison
    assert "eye_color" in comparison
    assert "birth_year" in comparison
    assert "gender" in comparison
