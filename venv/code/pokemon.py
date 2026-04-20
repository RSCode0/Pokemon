import requests
from entities import PokemonEntity

class Pokemon:
    def __init__(self, name):
        self.name = name
        self.stats = self.get_stats()
        self.entity = None
    
    def get_stats(self):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}")
        return response.json()

    def spawn_pokemon(self):
        self.entity = PokemonEntity(f"pokemons/{self.name}.png", 4, 4)
        return self.entity