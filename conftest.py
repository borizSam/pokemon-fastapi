import copy

import pytest

import main as app_module


@pytest.fixture(autouse=True)
def reset_pokemons():
    original = copy.deepcopy(app_module.pokemons)
    yield
    app_module.pokemons.clear()
    app_module.pokemons.extend(original)
