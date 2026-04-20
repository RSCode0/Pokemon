import pygame
from entities import Entity
from pokemon import Pokemon

class Player(Entity):
    def __init__(self, path, cols, rows, keys):
        super().__init__(path, cols, rows)
        self.keys = keys
        self.pokemon = Pokemon("pikachu")
    
    def update(self):
        super().update()
        self.check_move()
    
    def check_move(self):
        if pygame.K_q in self.keys:
            self.move_left()
            if not self.check_collision():
                self.rect.x -= 1
                self.pokemon.entity.move_left()
                if self.pokemon.entity.check_collision():
                    self.pokemon.entity.change_position("right", self.rect)
        elif pygame.K_d in self.keys:
            self.move_right()
            if not self.check_collision():
                self.rect.x += 1
                self.pokemon.entity.move_right()
                if self.pokemon.entity.check_collision():
                    self.pokemon.entity.change_position("left", self.rect)
        elif pygame.K_s in self.keys:
            self.move_down()
            if not self.check_collision():
                self.rect.y += 1
                self.pokemon.entity.move_down()
                if self.pokemon.entity.check_collision():
                    self.pokemon.entity.change_position("top", self.rect)
        elif pygame.K_z in self.keys:
            self.move_up()
            if not self.check_collision():
                self.rect.y -= 1
                self.pokemon.entity.move_up()
                if self.pokemon.entity.check_collision():
                    self.pokemon.entity.change_position("bottom", self.rect)

    

    
