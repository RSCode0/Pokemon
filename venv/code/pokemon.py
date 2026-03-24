import requests

from entities import PokemonEntity

class Pokemon:
    def __init__(self, name: str):
        self.name: str = name
        self.infos = self.get_stats()
        self.entity: PokemonEntity | None = None

    def get_stats(self):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}")
        return response.json()

    def spawn_pokemon(self):
        self.entity = PokemonEntity(f"/pokemons/{self.name}.png", 4, 4)
        return self.entity
    
    @staticmethod
    def create_pokemon(name):
        return Pokemon(name)