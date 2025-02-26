import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0, 150, 0)):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bamboo(pygame.sprite.Sprite):
    def __init__(self, x, y, height):
        super().__init__()
        self.image = pygame.Surface([10, height])
        self.image.fill((139, 69, 19))  # Brown color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class AnimalCage(pygame.sprite.Sprite):
    def __init__(self, x, y, animal_type="generic"):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill((150, 150, 150))  # Gray cage
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animal_type = animal_type
        self.is_open = False
        
    def open_cage(self):
        self.is_open = True
        # Change appearance when opened
        self.image.fill((100, 100, 100))  # Darker gray for open cage

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_start, patrol_end):
        super().__init__()
        self.image = pygame.Surface([30, 50])
        self.image.fill((255, 0, 0))  # Red for enemy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Patrol path
        self.patrol_start = patrol_start
        self.patrol_end = patrol_end
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        
    def update(self):
        # Move along patrol path
        self.rect.x += self.speed * self.direction
        
        # Change direction at patrol endpoints
        if self.rect.x >= self.patrol_end:
            self.direction = -1
        elif self.rect.x <= self.patrol_start:
            self.direction = 1 