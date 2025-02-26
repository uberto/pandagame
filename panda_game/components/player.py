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
        self.climb_direction = 0  # 0 = not climbing, -1 = up, 1 = down
        self.speed = 5
        self.climb_speed = 3  # Separate speed for climbing
        self.jump_power = 15
        self.gravity = 0.8
        
    def update(self, platforms=None, bamboo=None):
        # Store previous position for collision resolution
        prev_x = self.rect.x
        prev_y = self.rect.y
        
        # Check for bamboo climbing before applying gravity
        self.climbing = False
        if bamboo:
            for stalk in bamboo:
                # Check if panda is touching bamboo
                if self.rect.colliderect(stalk.rect):
                    self.climbing = True
                    break
        
        # Apply gravity if not climbing
        if not self.climbing:
            self.velocity_y += self.gravity
            self.climb_direction = 0  # Reset climb direction when not climbing
        else:
            # Apply continuous climbing if a direction is set
            if self.climb_direction != 0:
                self.velocity_y = self.climb_direction * self.climb_speed
            else:
                # When on bamboo but not actively climbing, slow down vertical movement
                self.velocity_y *= 0.5
        
        # Update horizontal position
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
                    # Only handle platform collisions if not climbing or if the collision is from above
                    if not self.climbing or self.velocity_y > 0:
                        if self.velocity_y > 0:  # Falling
                            self.rect.bottom = platform.rect.top
                            self.velocity_y = 0
                            self.on_ground = True
                        elif self.velocity_y < 0:  # Jumping
                            # Only block upward movement if the panda's head is close to the platform
                            if prev_y > platform.rect.bottom - 10:
                                self.rect.top = platform.rect.bottom
                                self.velocity_y = 0
            
    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_power
            self.on_ground = False
            
    def move(self, direction):
        self.velocity_x = direction * self.speed
        
    def climb(self, direction):
        if self.climbing:
            self.climb_direction = direction  # Set climbing direction
            self.velocity_y = direction * self.climb_speed
    
    def stop_climbing(self):
        """Stop vertical movement when climbing keys are released"""
        if self.climbing:
            self.climb_direction = 0
            self.velocity_y = 0 