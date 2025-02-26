import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        # Temporary rectangle for the panda (will be replaced with proper sprite)
        self.image = pygame.Surface([40, 40])
        self.image.fill((255, 255, 255))  # White
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        
        # Movement properties
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.climbing = False
        self.speed = 5
        self.jump_power = 15
        self.gravity = 0.8
        
    def update(self, platforms=None, bamboo=None):
        # Apply gravity if not climbing
        if not self.climbing:
            self.velocity_y += self.gravity
        
        # Update position
        self.rect.x += self.velocity_x
        
        # Check for platform collisions after horizontal movement
        if platforms:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.velocity_x > 0:  # Moving right
                        self.rect.right = platform.rect.left
                    elif self.velocity_x < 0:  # Moving left
                        self.rect.left = platform.rect.right
        
        # Update vertical position
        self.rect.y += self.velocity_y
        
        # Check for platform collisions after vertical movement
        if platforms:
            self.on_ground = False
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.velocity_y > 0:  # Falling
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                    elif self.velocity_y < 0:  # Jumping
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0
        
        # Check for bamboo climbing
        if bamboo:
            self.climbing = False
            for stalk in bamboo:
                if self.rect.colliderect(stalk.rect):
                    self.climbing = True
                    # Allow vertical movement on bamboo
                    if self.velocity_y != 0:
                        self.velocity_y = self.velocity_y / 2  # Slower climbing
            
    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_power
            self.on_ground = False
            
    def move(self, direction):
        self.velocity_x = direction * self.speed
        
    def climb(self, direction):
        if self.climbing:
            self.velocity_y = direction * (self.speed / 2)  # Slower climbing speed 