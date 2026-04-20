import pyscroll
import pytmx
import pygame

class Map:
    def __init__(self, screen):
        self.map = ""
        self.screen = screen
        self.tmx_data = None
        self.map_data = None
        self.map_layer = None
        self.group = None
        self.player = None
        self.player_spawn = None
        self.collisions = []
        self.tps = None
        self.load_map("map_0")
    
    def update(self):
        self.group.update()
        self.check_tp()
        self.group.center(self.player.rect)
        self.group.draw(self.screen)

    def load_map(self, map):
        self.tmx_data = pytmx.load_pygame(f"venv/assets/map/{map}.tmx")
        self.player_spawn = self.get_spawn()
        self.map = map
        self.tps = self.get_tps()
        self.get_collision()
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.screen.get_size())
        self.zoom_map()
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        if self.player:
            self.add_player(self.player)
            self.group.add(self.player.pokemon.entity)
    
    def zoom_map(self):
        if self.map.startswith(("house", "hospital")):
            self.map_layer.zoom = 5
        else:
            self.map_layer.zoom = 3

    def get_collision(self):
        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.collisions.append(pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height))
    
    def get_spawn(self):
        for obj in self.tmx_data.objects:
            if obj.name.split(" ")[0] == "spawn" and obj.name.split(" ")[1] == self.map:
                return [obj.x, obj.y]
        for obj in self.tmx_data.objects:
            if obj.name == "player_spawn":
                return [obj.x, obj.y]
        
    def get_tps(self):
        tps = []
        for obj in self.tmx_data.objects:
            if obj.name.split(" ")[0] == "tp":
                tps.append({
                    "rect": pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height),
                    "name": str(obj.name).split(" ")[1]
                })
        return tps

    def check_tp(self):
        for tp in self.tps:
            if self.player.rect.colliderect(tp["rect"]):
                self.load_map(tp["name"])
        
    def add_player(self, player):
        self.player = player
        self.group.add(self.player)
        self.player.rect.center = self.player_spawn
        self.player.collisions = self.collisions
    
    def add_pokemon(self):
        if self.player.pokemon:
            self.group.add(self.player.pokemon.spawn_pokemon())
            self.player.pokemon.entity.collisions = self.collisions
            self.player.pokemon.entity.rect.left = self.player.rect.right
            self.player.pokemon.entity.rect.top = self.player.rect.bottom