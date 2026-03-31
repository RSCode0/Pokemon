import pygame
import pyscroll
import pytmx
from sys import exit

from player import Player

pygame.init()

class Game:
    def __init__(self):
        self.keys = []
        
        self.display_surf = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.framerate = 60
        self.dt = 0
        self.running = True

        self.player = Player("spritesheet/ash_atchoum_walk.png", 4, 4, self.keys)

        self.tmx_data = pytmx.load_pygame("venv/assets/map/map_0.tmx")
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.display_surf.get_size())
        self.map_layer.zoom = 3
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

        self.group.add(self.player)
        
    
    def run(self):
        while self.running:
            self.get_input()
            self.player.dt = self.dt
            self.group.update()
            self.group.center(self.player.rect)
            self.group.draw(self.display_surf)
            pygame.display.update()
            self.dt = self.clock.tick(self.framerate) / 1000
    
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if not event.key in self.keys:
                    self.keys.append(event.key)
            if event.type == pygame.KEYUP:
                if event.key in self.keys:
                    self.keys.remove(event.key)
            