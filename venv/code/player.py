
import pygame
from entities import Entity

class Player(Entity):
    def __init__(self, path, cols, rows, keys):
        super().__init__(path, cols, rows)
        self.keys = keys
    
    def update(self):
        self.check_move()
    
    def check_move(self):
        if pygame.K_q in self.keys:
            self.move_left()
        elif pygame.K_d in self.keys:
            self.move_right()
        elif pygame.K_s in self.keys:
            self.move_down()
        elif pygame.K_z in self.keys:
            self.move_up()

    

    
