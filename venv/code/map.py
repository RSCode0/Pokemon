import pytmx
import pyscroll
import pygame

from screen import Screen
from player import Player
from pokemon import Pokemon
from keylogs import Keylogs
from entities import Entity

class Map:
    def __init__(self, screen: Screen, map, keylogs: Keylogs):
        self.screen: Screen = screen
        self.keylogs: Keylogs = keylogs
        self.map = map
        self.tmx_data = None
        self.map_data = None
        self.map_layer = None
        self.group = None
        self.pnj = {}
        self.player_spawn: tuple[int] | None= None
        self.collisions: list[pygame.rect.Rect] | None = None
        self.tps: list[dict[pygame.rect.Rect, str]] | None = None
        self.player: Player | None = None
        self.selected_pokemon: Pokemon | None = None
        self.active_pokemon: bool = False
        self.load_map(map)
    
    def load_map(self, map: str):
        self.tmx_data = pytmx.load_pygame(f"venv/assets/map/{map}.tmx")
        self.collisions = self.get_collisions()
        self.player_spawn = self.get_spawn()
        self.map = map
        self.tps = self.get_tps()
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, (1280, 780))
        if map.startswith("house"):
            self.map_layer.zoom = 5
        else:
            self.map_layer.zoom = 3
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)

        self.add_pnj("sprite/pnj1_map_0.png", self.player_spawn)
        
        if self.player:
            self.add_player(self.player)
        
    def get_collisions(self):
        collisions: list[pygame.rect.Rect] = []
        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                collisions.append(pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height))
        return collisions

    def get_tps(self):
        tps: list[dict[pygame.rect.Rect, str]] = []
        for obj in self.tmx_data.objects:
            if str(obj.name).split(" ")[0] == "tp":
                tps.append({
                    "rect": pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height),
                    "name": str(obj.name).split(" ")[1]
                })
        return tps
    
    def update(self):
        self.group.update()
        self.group.center(self.player.rect)
        self.group.draw(self.screen.get_display())
        if not self.active_pokemon:
            if self.keylogs.is_pressed(pygame.K_e):
                self.add_pokemon()
                self.keylogs.remove_key(pygame.K_e)
        else:
            if self.keylogs.is_pressed(pygame.K_e):
                self.remove_pokemon()
                self.keylogs.remove_key(pygame.K_e)

    def get_spawn(self):
        for obj in self.tmx_data.objects:
            if str(obj.name).endswith(self.map) and str(obj.name).startswith("spawn"):
                return [int(obj.x,), int(obj.y)]
        for obj in self.tmx_data.objects:
            if obj.name == "player_spawn":
                return [int(obj.x), int(obj.y)]
        
    def add_player(self, player: Player):
        self.player: Player = player
        self.player.add_collisions(self.collisions)
        self.player.rect.center = self.player_spawn
        self.selected_pokemon = self.player.pokemon
        self.group.add(player)
    
    def check_tp(self):
        for tp in self.tps:
            if self.player.rect.colliderect(tp["rect"]):
                self.load_map(tp["name"])

    def add_pokemon(self):
        self.group.add(self.selected_pokemon.spawn_pokemon())
        self.active_pokemon = True
        self.selected_pokemon.entity.rect.left = self.player.rect.right
        self.selected_pokemon.entity.rect.top = self.player.rect.top
        self.selected_pokemon.entity.add_collisions(self.collisions)
    
    def remove_pokemon(self):
        self.group.remove(self.player.pokemon.entity)
        self.active_pokemon = False
    
    def add_pnj(self, pnj, co):
        self.pnj[pnj] = Entity(pnj, 4, 4)
        if self.map in pnj:
            self.group.add(self.pnj[pnj])
            self.pnj[pnj].rect.center = co
    



