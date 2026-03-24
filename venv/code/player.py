import pygame

from entities import Entity
from keylogs import Keylogs
from pokemon import Pokemon

class Player(Entity):
    def __init__(self, spritesheet: str, rows: int, cols: int, keylogs: Keylogs):
        super().__init__(spritesheet, rows, cols)
        self.keylogs: Keylogs = keylogs
        self.pokemon: Pokemon | None = Pokemon.create_pokemon("pikachu")
    
    def update(self):
        super().update()
        self.check_input()
    
    def check_input(self):
        if self.keylogs.is_pressed(pygame.K_z):
            self.move_up()
            if not self.check_collision():
                self.rect.y -= 1
                if self.pokemon.entity:
                    self.pokemon.entity.move_up()
                    if self.pokemon.entity.check_collision():
                        self.pokemon.entity.change_position("down", self.rect)
        elif self.keylogs.is_pressed(pygame.K_s):
            self.move_down()
            if not self.check_collision():
                self.rect.y += 1
                if self.pokemon.entity:
                    self.pokemon.entity.move_down()
                    if self.pokemon.entity.check_collision():
                        self.pokemon.entity.change_position("top", self.rect)
        elif self.keylogs.is_pressed(pygame.K_q):
            self.move_left()
            if not self.check_collision():
                self.rect.x -= 1
                if self.pokemon.entity:
                    self.pokemon.entity.move_left()
                    if self.pokemon.entity.check_collision():
                        self.pokemon.entity.change_position("right", self.rect)
        elif self.keylogs.is_pressed(pygame.K_d):
            self.move_right()
            if not self.check_collision():
                self.rect.x += 1
                if self.pokemon.entity: 
                    self.pokemon.entity.move_right()
                    if self.pokemon.entity.check_collision():
                        self.pokemon.entity.change_position("left", self.rect)
        
    def move(self):
        if self.direction == "up":
            self.move_up()
        elif self.direction == "down":
            self.move_down()
        elif self.direction == "left":
            self.move_left()
        elif self.direction == "right":
            self.move_right()