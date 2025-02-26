import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=None):
        super().__init__()
        self.image = pygame.Surface([width, height])
        
        # Use a more natural green color for platforms if none specified
        if color is None:
            color = (76, 153, 0)  # Grass green
            
        self.image.fill(color)
        
        # Add some texture to the platform (simple grass effect)
        for i in range(0, width, 10):
            grass_height = 3
            pygame.draw.rect(self.image, (50, 120, 0), [i, 0, 5, grass_height])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bamboo(pygame.sprite.Sprite):
    def __init__(self, x, y, height=100):
        super().__init__()
        self.image = pygame.Surface([10, height], pygame.SRCALPHA)
        
        # Draw bamboo with segments
        segment_height = 20
        for i in range(0, height, segment_height):
            # Main bamboo stalk (light green)
            pygame.draw.rect(self.image, (150, 200, 70), [0, i, 10, segment_height])
            
            # Darker green rings at segment joints
            if i > 0:
                pygame.draw.rect(self.image, (100, 160, 50), [0, i, 10, 3])
            
            # Highlight on left side
            pygame.draw.rect(self.image, (180, 220, 100), [1, i, 2, segment_height])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - height  # Position from the bottom up

class AnimalCage(pygame.sprite.Sprite):
    def __init__(self, x, y, animal_type="generic"):
        super().__init__()
        self.image = pygame.Surface([50, 50], pygame.SRCALPHA)
        self.animal_type = animal_type
        self.is_open = False
        
        # Draw the cage
        self.draw_cage()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw_cage(self):
        """Draw the cage with or without an animal inside"""
        # Clear the surface
        self.image.fill((0, 0, 0, 0))  # Transparent
        
        cage_color = (150, 150, 150)  # Gray for closed cage
        if self.is_open:
            cage_color = (100, 100, 100)  # Darker gray for open cage
        
        # Cage base
        pygame.draw.rect(self.image, cage_color, [5, 35, 40, 10])
        
        # Cage bars
        if not self.is_open:
            for i in range(5, 45, 8):
                pygame.draw.rect(self.image, cage_color, [i, 5, 3, 35])
            
            # Cage top
            pygame.draw.rect(self.image, cage_color, [5, 5, 40, 3])
            
            # Draw animal inside based on type
            if self.animal_type == "monkey":
                # Brown monkey
                pygame.draw.circle(self.image, (139, 69, 19), (25, 25), 10)  # Body
                pygame.draw.circle(self.image, (139, 69, 19), (25, 15), 7)   # Head
                pygame.draw.circle(self.image, (0, 0, 0), (22, 13), 2)       # Eye
                pygame.draw.circle(self.image, (0, 0, 0), (28, 13), 2)       # Eye
            elif self.animal_type == "tiger":
                # Orange tiger with stripes
                pygame.draw.circle(self.image, (255, 165, 0), (25, 25), 10)  # Body
                pygame.draw.circle(self.image, (255, 165, 0), (25, 15), 7)   # Head
                # Stripes
                pygame.draw.line(self.image, (0, 0, 0), (20, 25), (30, 25), 2)
                pygame.draw.line(self.image, (0, 0, 0), (22, 20), (28, 20), 2)
                pygame.draw.circle(self.image, (0, 0, 0), (22, 13), 2)       # Eye
                pygame.draw.circle(self.image, (0, 0, 0), (28, 13), 2)       # Eye
            else:
                # Generic animal (blue)
                pygame.draw.circle(self.image, (100, 100, 255), (25, 25), 10)
        else:
            # Open cage door (bent bars)
            pygame.draw.arc(self.image, cage_color, [0, 5, 20, 30], 0, 3.14/2, 3)
            pygame.draw.arc(self.image, cage_color, [15, 0, 20, 30], 3.14/2, 3.14, 3)
    
    def open(self):
        """Open the cage and free the animal (new method name)"""
        self.open_cage()
        
    def open_cage(self):
        """Open the cage and free the animal"""
        if not self.is_open:
            self.is_open = True
            self.draw_cage()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_boundary_left=None, patrol_boundary_right=None, patrol_start=None, patrol_end=None):
        super().__init__()
        self.image = pygame.Surface([30, 50], pygame.SRCALPHA)
        self.draw_zookeeper()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Handle both parameter naming styles for backward compatibility
        if patrol_boundary_left is not None and patrol_boundary_right is not None:
            self.patrol_start = patrol_boundary_left
            self.patrol_end = patrol_boundary_right
        else:
            # Fall back to old parameter names if provided
            self.patrol_start = patrol_start if patrol_start is not None else x - 100
            self.patrol_end = patrol_end if patrol_end is not None else x + 100
        
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        
        # For animation
        self.facing_right = True
        
    def draw_zookeeper(self):
        """Draw a zookeeper character"""
        # Clear the surface
        self.image.fill((0, 0, 0, 0))  # Transparent
        
        # Body (blue uniform)
        pygame.draw.rect(self.image, (50, 50, 150), [5, 15, 20, 30])
        
        # Head
        pygame.draw.circle(self.image, (255, 200, 150), (15, 10), 10)  # Skin tone
        
        # Hat
        pygame.draw.rect(self.image, (30, 30, 100), [5, 2, 20, 5])
        
        # Eyes
        pygame.draw.circle(self.image, (0, 0, 0), (12, 8), 2)
        pygame.draw.circle(self.image, (0, 0, 0), (18, 8), 2)
        
        # Mouth
        pygame.draw.line(self.image, (0, 0, 0), (12, 14), (18, 14), 1)
        
        # Arms
        pygame.draw.rect(self.image, (50, 50, 150), [0, 20, 5, 15])  # Left arm
        pygame.draw.rect(self.image, (50, 50, 150), [25, 20, 5, 15])  # Right arm
        
        # Legs
        pygame.draw.rect(self.image, (0, 0, 100), [5, 45, 8, 5])  # Left leg
        pygame.draw.rect(self.image, (0, 0, 100), [17, 45, 8, 5])  # Right leg
        
    def update(self):
        # Move along patrol path
        self.rect.x += self.speed * self.direction
        
        # Update facing direction
        if self.direction > 0:
            self.facing_right = True
        else:
            self.facing_right = False
        
        # Change direction at patrol endpoints
        if self.rect.x >= self.patrol_end:
            self.direction = -1
        elif self.rect.x <= self.patrol_start:
            self.direction = 1 