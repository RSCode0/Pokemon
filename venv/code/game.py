import pygame
from map import Map
from sys import exit

from player import Player
from save import Save
from inventory import InventoryBar

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
        Save.load_inventory(self.player.inventory)
        self.inventory_bar = InventoryBar(self.display_surf, self.player.inventory)
        self.map = Map(self.display_surf, self.keys)
        self.map.add_player(self.player)
        if self.player.pokemon:
            self.map.add_pokemon()
        
    def run(self):
        while self.running:
            self.get_input()
            self.player.dt = self.dt
            self.player.pokemon.entity.dt = self.dt
            self.map.update()
            self.inventory_bar.draw_inventory()
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
                    self.inventory_bar.select_item(event.key)
            if event.type == pygame.KEYUP:
                if event.key in self.keys:
                    self.keys.remove(event.key)
            