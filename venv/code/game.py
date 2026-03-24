import pygame
from sys import exit

pygame.init()

from screen import Screen
from map import Map
from player import Player
from keylogs import Keylogs

class Game:
    def __init__(self):
        self.running = True
        self.screen: Screen = Screen()
        self.keylogs: Keylogs = Keylogs()
        self.map = Map(self.screen, "map_0", self.keylogs)
        self.player: Player = Player("/sprite/ash_atchoum_walk.png", 4, 4, self.keylogs)
        self.map.add_player(self.player)
    
    def run(self):
        while self.running:
            self.player.dt = self.screen.dt
            if self.player.pokemon.entity:
                self.player.pokemon.entity.dt = self.screen.dt
            self.screen.update()
            self.get_inputs()
            self.map.check_tp()
            self.map.update()
        
    def get_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                self.keylogs.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.keylogs.remove_key(event.key)
    