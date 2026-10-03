from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Pokemon API"
    assert body["total"] == 20


def test_list_pokemon():
    response = client.get("/pokemon")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 20
    assert any(p["name"] == "Pikachu" for p in body)


def test_get_pokemon_by_id_found():
    response = client.get("/pokemon/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Bulbasaur"


def test_get_pokemon_by_id_not_found():
    response = client.get("/pokemon/9999")
    assert response.status_code == 404


def test_get_pokemon_by_name():
    response = client.get("/pokemon/name/Charizard")
    assert response.status_code == 200
    assert response.json()["id"] == 6

    response = client.get("/pokemon/name/charizard")
    assert response.status_code == 200
    assert response.json()["id"] == 6


def test_get_pokemon_by_name_not_found():
    response = client.get("/pokemon/name/Missingno")
    assert response.status_code == 404


def test_filter_by_type():
    response = client.get("/pokemon", params={"type": "Fire"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3
    assert all(p["type"] == "Fire" for p in body)


def test_filter_by_name_partial():
    response = client.get("/pokemon", params={"name": "char"})
    assert response.status_code == 200
    body = response.json()
    assert {p["name"] for p in body} == {"Charmander", "Charmeleon", "Charizard"}


def test_create_pokemon():
    payload = {"name": "Mewtwo", "type": "Psychic", "hp": 106, "attack": 110, "defense": 90, "speed": 130}
    response = client.post("/pokemon", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 21
    assert body["name"] == "Mewtwo"

    response = client.get("/pokemon/21")
    assert response.status_code == 200


def test_update_pokemon():
    payload = {"name": "Raichu", "type": "Electric", "hp": 60, "attack": 90, "defense": 55, "speed": 110}
    response = client.put("/pokemon/11", json=payload)
    assert response.status_code == 200
    assert response.json()["attack"] == 90

    response = client.get("/pokemon/11")
    assert response.json()["name"] == "Raichu"


def test_update_pokemon_not_found():
    payload = {"name": "Ghost", "type": "Ghost", "hp": 1, "attack": 1, "defense": 1, "speed": 1}
    response = client.put("/pokemon/9999", json=payload)
    assert response.status_code == 404


def test_delete_pokemon():
    response = client.delete("/pokemon/20")
    assert response.status_code == 204

    response = client.get("/pokemon/20")
    assert response.status_code == 404


def test_delete_pokemon_not_found():
    response = client.delete("/pokemon/9999")
    assert response.status_code == 404
