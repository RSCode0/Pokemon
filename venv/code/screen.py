import pygame

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 780))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.framerate: int = 60
        self.dt: float = 0
    
    def update(self):
        self.dt = self.clock.tick(self.framerate) / 1000
        pygame.display.flip()
        pygame.display.update()

    def get_size(self):
        return self.screen.get_size()

    def get_display(self):
        return self.screen