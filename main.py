from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Pokemon API", version="1.0.0")


class Pokemon(BaseModel):
    id: int
    name: str
    type: str
    hp: int
    attack: int
    defense: int
    speed: int


class PokemonCreate(BaseModel):
    name: str
    type: str
    hp: int
    attack: int
    defense: int
    speed: int


pokemons: list[Pokemon] = [
    Pokemon(id=1, name="Bulbasaur", type="Grass", hp=45, attack=49, defense=49, speed=45),
    Pokemon(id=2, name="Ivysaur", type="Grass", hp=60, attack=62, defense=63, speed=60),
    Pokemon(id=3, name="Venusaur", type="Grass", hp=80, attack=82, defense=83, speed=80),
    Pokemon(id=4, name="Charmander", type="Fire", hp=39, attack=52, defense=43, speed=65),
    Pokemon(id=5, name="Charmeleon", type="Fire", hp=58, attack=64, defense=58, speed=80),
    Pokemon(id=6, name="Charizard", type="Fire", hp=78, attack=84, defense=78, speed=100),
    Pokemon(id=7, name="Squirtle", type="Water", hp=44, attack=48, defense=65, speed=43),
    Pokemon(id=8, name="Wartortle", type="Water", hp=59, attack=63, defense=80, speed=58),
    Pokemon(id=9, name="Blastoise", type="Water", hp=79, attack=83, defense=100, speed=78),
    Pokemon(id=10, name="Pikachu", type="Electric", hp=35, attack=55, defense=40, speed=90),
    Pokemon(id=11, name="Raichu", type="Electric", hp=60, attack=90, defense=55, speed=110),
    Pokemon(id=12, name="Jigglypuff", type="Normal", hp=115, attack=45, defense=20, speed=20),
    Pokemon(id=13, name="Meowth", type="Normal", hp=40, attack=45, defense=35, speed=90),
    Pokemon(id=14, name="Psyduck", type="Water", hp=50, attack=52, defense=48, speed=55),
    Pokemon(id=15, name="Machop", type="Fighting", hp=70, attack=80, defense=50, speed=35),
    Pokemon(id=16, name="Geodude", type="Rock", hp=40, attack=80, defense=100, speed=20),
    Pokemon(id=17, name="Gastly", type="Ghost", hp=30, attack=35, defense=30, speed=80),
    Pokemon(id=18, name="Onix", type="Rock", hp=35, attack=45, defense=160, speed=70),
    Pokemon(id=19, name="Eevee", type="Normal", hp=55, attack=55, defense=50, speed=55),
    Pokemon(id=20, name="Snorlax", type="Normal", hp=160, attack=110, defense=65, speed=30),
]


def next_id() -> int:
    return max((p.id for p in pokemons), default=0) + 1


@app.get("/")
def root():
    return {"message": "Pokemon API", "docs": "/docs", "total": len(pokemons)}


@app.get("/pokemon", response_model=list[Pokemon])
def list_pokemon(
    type: Optional[str] = Query(None, description="Filtrar por tipo"),
    name: Optional[str] = Query(None, description="Buscar por nombre (parcial)"),
):
    result = pokemons
    if type:
        result = [p for p in result if p.type.lower() == type.lower()]
    if name:
        result = [p for p in result if name.lower() in p.name.lower()]
    return result


@app.get("/pokemon/{pokemon_id}", response_model=Pokemon)
def get_pokemon(pokemon_id: int):
    for p in pokemons:
        if p.id == pokemon_id:
            return p
    raise HTTPException(status_code=404, detail="Pokemon no encontrado")


@app.get("/pokemon/name/{name}", response_model=Pokemon)
def get_pokemon_by_name(name: str):
    for p in pokemons:
        if p.name.lower() == name.lower():
            return p
    raise HTTPException(status_code=404, detail="Pokemon no encontrado")


@app.post("/pokemon", response_model=Pokemon, status_code=201)
def create_pokemon(data: PokemonCreate):
    pokemon = Pokemon(id=next_id(), **data.model_dump())
    pokemons.append(pokemon)
    return pokemon


@app.put("/pokemon/{pokemon_id}", response_model=Pokemon)
def update_pokemon(pokemon_id: int, data: PokemonCreate):
    for i, p in enumerate(pokemons):
        if p.id == pokemon_id:
            pokemons[i] = Pokemon(id=pokemon_id, **data.model_dump())
            return pokemons[i]
    raise HTTPException(status_code=404, detail="Pokemon no encontrado")


@app.delete("/pokemon/{pokemon_id}", status_code=204)
def delete_pokemon(pokemon_id: int):
    for i, p in enumerate(pokemons):
        if p.id == pokemon_id:
            pokemons.pop(i)
            return
    raise HTTPException(status_code=404, detail="Pokemon no encontrado")
