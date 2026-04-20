import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, path, cols, rows):
        super().__init__()
        self.spritesheet = pygame.image.load(f"venv/assets/{path}").convert_alpha()
        self.spritesheet = pygame.transform.scale_by(self.spritesheet, 0.5)
        self.width = self.spritesheet.get_size()[0]
        self.height = self.spritesheet.get_size()[1]
        self.cols = cols
        self.rows = rows
        self.frame_width = self.width // cols
        self.frame_height = self.height // rows
        self.dt = 0
        self.frame_index = 0
        self.image = self.spritesheet.subsurface((0, 0, self.frame_width, self.frame_height))
        self.all_images = self.get_all_images()
        self.rect = self.image.get_rect()
        self.hitbox = pygame.rect.Rect((0, 0, self.frame_width, self.frame_height // 2))
        self.collisions = None
    
    def update(self):
        self.hitbox.midbottom = self.rect.midbottom
    
    def move_right(self):
        self.hitbox.x += 1
        self.animation("right")
    
    def move_left(self):
        self.hitbox.x -= 1
        self.animation("left")

    def move_up(self):
        self.hitbox.y -= 1
        self.animation("up")
    
    def move_down(self):
        self.hitbox.y += 1
        self.animation("down")

    def animation(self, direction):
        self.frame_index += 7 * self.dt
        self.image = self.all_images[direction][int(self.frame_index) % len(self.all_images[direction])]
    
    def check_collision(self):
        if not self.collisions:
            return False
        for collision in self.collisions:
            if self.hitbox.colliderect(collision):
                return True
        return False
    
    def get_all_images(self):
        frames = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }

        for row, direction in enumerate(frames.keys()):
            for col in range(self.cols):
                frames[direction].append(self.spritesheet.subsurface(((self.width // self.cols) * col, (self.height // self.rows) * row, self.frame_width, self.frame_height)))

        return frames

class PokemonEntity(Entity):
    def __init__(self, path, cols, rows):
        super().__init__(path, cols, rows)
    
    def move_right(self):
        self.rect.x += 1
        self.animation("right")
    
    def move_left(self):
        self.rect.x -= 1
        self.animation("left")

    def move_up(self):
        self.rect.y -= 1
        self.animation("up")
    
    def move_down(self):
        self.rect.y += 1
        self.animation("down")
    
    def change_position(self, player_side, player_rect):
        if player_side == "top":
            self.rect.bottom = player_rect.top
            self.rect.left = player_rect.left
        elif player_side == "bottom":
            self.rect.top = player_rect.bottom
            self.rect.left = player_rect.left
        elif player_side == "left":
            self.rect.right = player_rect.left
            self.rect.top = player_rect.top
        elif player_side == "right":
            self.rect.left = player_rect.right
            self.rect.top = player_rect.top