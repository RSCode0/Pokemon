import pygame
import json

class Entity(pygame.sprite.Sprite):
    def __init__(self, path, cols, rows):
        super().__init__()
        self.spritesheet = pygame.image.load(f"venv/assets/{path}").convert_alpha()
        if self.spritesheet.get_size()[0] > 150:
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

class NPC(Entity):
    def __init__(self, path, cols, rows, name):
        super().__init__(path, cols, rows)
        self.name = name
        self.get_rect()
        self.last_dialogue_id = ""
        self.font = pygame.font.Font(None, 30)
        self.npc_dialogues = []
        self.player_dialogues = []
        self.npc_dialogue_index = 0
        self.player_dialogue_index = 0
        self.npc_turn = True
        self.dialogue_active = False
        self.current_text = ""
    
    def update(self):
        self.hitbox.bottomleft = self.rect.bottomleft
        bounding = self.image.get_bounding_rect()
        self.hitbox.midbottom = (self.rect.x + bounding.centerx, self.rect.y + bounding.bottom)

    def get_rect(self):
        self.hitbox = pygame.rect.Rect(0, 0, self.frame_width, self.frame_height)
        bounding = self.image.get_bounding_rect()
        self.hitbox = pygame.rect.Rect(0, 0, bounding.width * 0.7, 24)
    
    def load_dialogues(self):
        with open("venv/code/json/dialogues.json", "r", encoding="utf-8") as file:
            data_dialogues = json.load(file)
            with open("venv/code/json/save.json") as file:
                data_save = json.load(file)
                self.last_dialogue_id = data_save["dialogues"][self.name]
                self.npc_dialogues = data_dialogues[self.name][self.last_dialogue_id]["text"]
                self.player_dialogues = data_dialogues[self.name][self.last_dialogue_id]["response"]
    
    def active_dialogue(self, keys, screen):
        if self.dialogue_active:
            self.draw_current_dialogue(screen)
            if pygame.K_SPACE in keys:
                self.advance_dialogue()
                keys.remove(pygame.K_SPACE)
        else:
            if pygame.K_SPACE in keys:
                self.start_dialogue()
                self.dialogue_active = True
                keys.remove(pygame.K_SPACE)
    
    def next_section(self):
        next_section_index = None
        next_section_name = self.last_dialogue_id
        with open("venv/code/json/dialogues.json") as file:
            data_dialogues = json.load(file)
            for i, key in enumerate(data_dialogues[self.name].keys()):
                if next_section_index == i:
                    next_section_name = key
                    break
                if key == self.last_dialogue_id:
                    if i < len(data_dialogues[self.name].keys()):
                        next_section_index = i + 1
        self.save_progression(next_section_name)
        
    def save_progression(self, next_section_name):
        with open("venv/code/json/save.json") as file:
            data_save = json.load(file)
        
        data_save["dialogues"][self.name] = next_section_name
        
        with open("venv/code/json/save.json", "w", encoding="utf-8") as file:
            json.dump(data_save, file, ensure_ascii=False, indent=4)
    
    def draw_current_dialogue(self, screen):
        if self.current_text:
            self.draw_text(self.current_text, screen)
    
    def draw_text(self, text, screen):
        words = text.split(" ")
        ligne = []
        current_line = ""
    
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < 1280 - 90:
                current_line = test_line
            else:
                ligne.append(current_line)
                current_line = word + " "
        
        ligne.append(current_line)
        
        line_height = self.font.get_linesize()
        pygame.draw.rect(screen, (58, 158, 181), (40, 780 - 180, 1280 - 80, 100), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (40, 780 - 180, 1280 - 80, 100), 2, border_radius=10)
        for i, line in enumerate(ligne):
            screen.blit(self.font.render(line, True, (255, 255, 255) if self.npc_turn else (0, 0, 0)), (50, 780 - 160 + i * line_height))
    
    def advance_dialogue(self):
        if self.npc_dialogue_index == len(self.npc_dialogues) and self.player_dialogue_index == len(self.player_dialogues):
            self.next_section()
            self.dialogue_active = False
            return

        if self.npc_turn:
            if self.npc_dialogue_index < len(self.npc_dialogues):
                self.current_text = self.npc_dialogues[self.npc_dialogue_index]
                self.npc_dialogue_index += 1
                self.npc_turn = False
        else:
            if self.player_dialogue_index < len(self.player_dialogues):
                self.current_text = self.player_dialogues[self.player_dialogue_index]
                self.player_dialogue_index += 1
                self.npc_turn = True
            
    def start_dialogue(self):
        self.load_dialogues()
        self.npc_dialogue_index = 0
        self.player_dialogue_index = 0
        self.npc_turn = True
        self.advance_dialogue()