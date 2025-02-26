import pygame
import random
import math
from panda_game.components.objects import Platform, Bamboo, AnimalCage, Enemy

class Level:
    """A game level with platforms, enemies, and collectibles"""
    def __init__(self, player, level_num=1):
        # Sprite groups
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.bamboo_list = pygame.sprite.Group()
        self.cage_list = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()  # For beach edges and palm trees
        
        self.player = player
        self.level_num = level_num
        
        # Level dimensions
        self.level_width = 800  # Default width
        self.level_height = 600
        
        # Background
        self.background = pygame.Surface([800, 600])
        self.background.fill((135, 206, 235))  # Sky blue
        
        # Set up the level
        self.setup_level()
    
    def setup_level(self):
        """Set up the level layout based on level_num"""
        if self.level_num == 1:
            # Level 1 - Small island
            self.level_width = 1200
            
            # Add beach edges
            self.add_beach_edges()
            
            # Ground platforms
            ground_y = 500
            # Left section
            self.platform_list.add(Platform(0, ground_y, 400, 100))
            # Middle gap
            # Right section
            self.platform_list.add(Platform(550, ground_y, 650, 100))
            
            # Floating platforms
            self.platform_list.add(Platform(200, 400, 100, 20))
            self.platform_list.add(Platform(400, 350, 100, 20))
            self.platform_list.add(Platform(600, 300, 100, 20))
            self.platform_list.add(Platform(800, 350, 100, 20))
            self.platform_list.add(Platform(1000, 400, 100, 20))
            
            # Add some bamboo
            self.bamboo_list.add(Bamboo(300, 400))
            self.bamboo_list.add(Bamboo(700, 300))
            self.bamboo_list.add(Bamboo(900, 350))
            
            # Add animal cages
            self.cage_list.add(AnimalCage(250, 400, "monkey"))
            self.cage_list.add(AnimalCage(850, 350, "tiger"))
            
            # Add enemies
            enemy1 = Enemy(100, ground_y - 50, patrol_boundary_left=50, patrol_boundary_right=350)
            enemy2 = Enemy(700, ground_y - 50, patrol_boundary_left=600, patrol_boundary_right=900)
            self.enemy_list.add(enemy1)
            self.enemy_list.add(enemy2)
            
        elif self.level_num == 2:
            # Level 2 - Larger island with more challenges
            self.level_width = 2000
            
            # Add beach edges
            self.add_beach_edges()
            
            # Ground platforms with gaps
            ground_y = 500
            # Left section
            self.platform_list.add(Platform(0, ground_y, 500, 100))
            # First gap
            # Middle section
            self.platform_list.add(Platform(700, ground_y, 600, 100))
            # Second gap
            # Right section
            self.platform_list.add(Platform(1500, ground_y, 500, 100))
            
            # Floating platforms
            platform_positions = [
                (200, 400, 150, 20),
                (450, 350, 100, 20),
                (650, 400, 100, 20),
                (850, 300, 120, 20),
                (1050, 250, 100, 20),
                (1250, 300, 100, 20),
                (1450, 350, 100, 20),
                (1650, 400, 150, 20)
            ]
            
            for pos in platform_positions:
                self.platform_list.add(Platform(pos[0], pos[1], pos[2], pos[3]))
            
            # Add bamboo
            bamboo_positions = [(300, 400), (750, 400), (950, 300), (1150, 250), (1350, 300), (1750, 400)]
            for pos in bamboo_positions:
                self.bamboo_list.add(Bamboo(pos[0], pos[1]))
            
            # Add animal cages
            self.cage_list.add(AnimalCage(500, 350, "monkey"))
            self.cage_list.add(AnimalCage(1100, 250, "tiger"))
            self.cage_list.add(AnimalCage(1700, 400, "monkey"))
            
            # Add enemies
            enemy_positions = [
                (200, ground_y - 50, 100, 400),
                (800, ground_y - 50, 750, 1000),
                (1200, ground_y - 50, 1100, 1300),
                (1600, ground_y - 50, 1550, 1800)
            ]
            
            for pos in enemy_positions:
                enemy = Enemy(pos[0], pos[1], patrol_boundary_left=pos[2], patrol_boundary_right=pos[3])
                self.enemy_list.add(enemy)
    
    def add_beach_edges(self):
        """Add beach edges and palm trees to the level"""
        # Left beach edge
        left_edge = BeachEdge(0, 500, 100, "left")
        self.decorations.add(left_edge)
        
        # Right beach edge
        right_edge = BeachEdge(self.level_width - 100, 500, 100, "right")
        self.decorations.add(right_edge)
        
        # Add palm trees near the edges
        # Left side palm trees
        for i in range(2):
            x_pos = random.randint(20, 80)
            y_pos = 500 - random.randint(0, 20)
            palm = PalmTree(x_pos, y_pos)
            self.decorations.add(palm)
        
        # Right side palm trees
        for i in range(2):
            x_pos = self.level_width - random.randint(80, 140)
            y_pos = 500 - random.randint(0, 20)
            palm = PalmTree(x_pos, y_pos)
            self.decorations.add(palm)
    
    def update(self):
        """Update all sprites in the level"""
        self.platform_list.update()
        self.enemy_list.update()
        self.bamboo_list.update()
        self.cage_list.update()
        self.decorations.update()  # Update palm trees for animation
    
    def draw(self, screen, camera_x=0):
        """Draw the level and all sprites"""
        # Draw the background
        screen.blit(self.background, (0, 0))
        
        # Draw all sprite groups with camera offset
        for platform in self.platform_list:
            screen.blit(platform.image, (platform.rect.x - camera_x, platform.rect.y))
        
        for bamboo in self.bamboo_list:
            screen.blit(bamboo.image, (bamboo.rect.x - camera_x, bamboo.rect.y))
        
        for cage in self.cage_list:
            screen.blit(cage.image, (cage.rect.x - camera_x, cage.rect.y))
        
        # Draw decorations (beach edges and palm trees)
        for decoration in self.decorations:
            screen.blit(decoration.image, (decoration.rect.x - camera_x, decoration.rect.y))
        
        # Draw enemies with correct orientation
        for enemy in self.enemy_list:
            if enemy.facing_right:
                screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y))
            else:
                # Flip the enemy image if facing left
                flipped_image = pygame.transform.flip(enemy.image, True, False)
                screen.blit(flipped_image, (enemy.rect.x - camera_x, enemy.rect.y))


class BeachEdge(pygame.sprite.Sprite):
    """Beach edge decoration to indicate the island boundaries"""
    def __init__(self, x, y, width, side="left"):
        super().__init__()
        self.image = pygame.Surface([width, 100], pygame.SRCALPHA)
        
        # Sand colors
        sand_color = (240, 230, 140)  # Khaki/sand color
        dark_sand = (220, 210, 120)   # Slightly darker sand
        wet_sand = (200, 190, 110)    # Wet sand near water
        
        # Draw the beach edge
        if side == "left":
            # Left side beach (slopes down to the right)
            # Main sand area
            points = [(0, 0), (width, 50), (0, 50)]
            pygame.draw.polygon(self.image, sand_color, points)
            
            # Wet sand near water
            wet_points = [(0, 50), (width, 50), (0, 100)]
            pygame.draw.polygon(self.image, wet_sand, wet_points)
            
            # Add some texture (small dots and pebbles)
            for _ in range(15):
                dot_x = random.randint(0, width - 3)
                dot_y = random.randint(5, 45)
                dot_size = random.randint(1, 3)
                pygame.draw.circle(self.image, dark_sand, (dot_x, dot_y), dot_size)
            
            # Add some shells
            for _ in range(3):
                shell_x = random.randint(5, width - 10)
                shell_y = random.randint(30, 90)
                self.draw_shell(shell_x, shell_y, random.randint(0, 359))
                
        else:  # right side
            # Right side beach (slopes down to the left)
            # Main sand area
            points = [(0, 50), (width, 0), (width, 50)]
            pygame.draw.polygon(self.image, sand_color, points)
            
            # Wet sand near water
            wet_points = [(width, 50), (width, 100), (0, 50)]
            pygame.draw.polygon(self.image, wet_sand, wet_points)
            
            # Add some texture (small dots and pebbles)
            for _ in range(15):
                dot_x = random.randint(3, width - 1)
                dot_y = random.randint(5, 45)
                dot_size = random.randint(1, 3)
                pygame.draw.circle(self.image, dark_sand, (dot_x, dot_y), dot_size)
            
            # Add some shells
            for _ in range(3):
                shell_x = random.randint(5, width - 10)
                shell_y = random.randint(30, 90)
                self.draw_shell(shell_x, shell_y, random.randint(0, 359))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 50  # Adjust y position to account for taller image
    
    def draw_shell(self, x, y, rotation):
        """Draw a small decorative shell on the beach"""
        shell_color = (255, 240, 220)  # Off-white
        shell_highlight = (255, 250, 240)  # Lighter highlight
        
        # Create a small surface for the shell
        shell_surface = pygame.Surface((8, 6), pygame.SRCALPHA)
        
        # Draw the shell shape
        pygame.draw.ellipse(shell_surface, shell_color, [0, 0, 8, 6])
        pygame.draw.line(shell_surface, shell_highlight, (4, 0), (4, 6), 1)
        pygame.draw.line(shell_surface, shell_highlight, (2, 1), (2, 5), 1)
        pygame.draw.line(shell_surface, shell_highlight, (6, 1), (6, 5), 1)
        
        # Rotate the shell
        rotated_shell = pygame.transform.rotate(shell_surface, rotation)
        
        # Blit the shell onto the beach
        self.image.blit(rotated_shell, (x - rotated_shell.get_width()//2, y - rotated_shell.get_height()//2))


class PalmTree(pygame.sprite.Sprite):
    """Palm tree decoration for the beach edges"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([80, 120], pygame.SRCALPHA)
        self.animation_offset = random.randint(0, 100)  # Random offset for animation
        
        # Draw the trunk with a slight curve
        trunk_color = (139, 69, 19)  # Brown
        trunk_highlight = (160, 90, 40)  # Lighter brown for highlight
        
        # Curved trunk points
        curve_offset = 5
        trunk_points = [
            (35, 60),  # Top of trunk
            (40 + curve_offset, 80),  # Curve right
            (38 + curve_offset, 100),  # Curve right
            (35, 120),  # Bottom right
            (25, 120),  # Bottom left
            (22 - curve_offset, 100),  # Curve left
            (20 - curve_offset, 80),  # Curve left
            (25, 60)   # Back to top
        ]
        pygame.draw.polygon(self.image, trunk_color, trunk_points)
        
        # Trunk highlight
        highlight_points = [
            (30, 60),  # Top
            (33 + curve_offset//2, 80),  # Curve
            (31 + curve_offset//2, 100),  # Curve
            (30, 120),  # Bottom
            (28, 120),  # Bottom
            (27, 100),  # Straight down
            (27, 80),  # Straight down
            (28, 60)   # Back to top
        ]
        pygame.draw.polygon(self.image, trunk_highlight, highlight_points)
        
        # Draw the leaves
        self.draw_leaves()
        
        # Add coconuts
        coconut_color = (101, 67, 33)  # Dark brown
        coconut_highlight = (120, 85, 50)  # Lighter brown
        
        # Left coconut
        pygame.draw.circle(self.image, coconut_color, (25, 60), 6)
        pygame.draw.circle(self.image, coconut_highlight, (23, 58), 2)
        
        # Right coconut
        pygame.draw.circle(self.image, coconut_color, (40, 55), 5)
        pygame.draw.circle(self.image, coconut_highlight, (38, 53), 2)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Store initial position and time for animation
        self.initial_y = y
        self.time = 0
    
    def draw_leaves(self):
        """Draw the palm tree leaves"""
        leaf_color = (0, 128, 0)  # Green
        leaf_highlight = (50, 160, 50)  # Lighter green
        
        # Left leaves
        self.draw_leaf(30, 55, -30, leaf_color, leaf_highlight)
        self.draw_leaf(30, 50, -10, leaf_color, leaf_highlight)
        self.draw_leaf(30, 45, -50, leaf_color, leaf_highlight)
        
        # Right leaves
        self.draw_leaf(30, 55, 30, leaf_color, leaf_highlight)
        self.draw_leaf(30, 50, 10, leaf_color, leaf_highlight)
        self.draw_leaf(30, 45, 50, leaf_color, leaf_highlight)
    
    def draw_leaf(self, x, y, angle, color, highlight_color):
        """Draw a single palm leaf at the given angle"""
        # Create a surface for the leaf
        leaf_length = 40
        leaf_width = 15
        leaf_surface = pygame.Surface((leaf_length, leaf_width), pygame.SRCALPHA)
        
        # Draw the leaf shape
        points = [
            (0, leaf_width//2),  # Base
            (leaf_length//4, leaf_width//4),  # Top curve
            (leaf_length, 0),  # Tip
            (leaf_length//4, 3*leaf_width//4),  # Bottom curve
        ]
        pygame.draw.polygon(leaf_surface, color, points)
        
        # Add a highlight along the center
        highlight_points = [
            (0, leaf_width//2),
            (leaf_length//4, leaf_width//2 - 1),
            (leaf_length - 5, leaf_width//2 - 1),
            (leaf_length - 5, leaf_width//2 + 1),
            (leaf_length//4, leaf_width//2 + 1)
        ]
        pygame.draw.polygon(leaf_surface, highlight_color, highlight_points)
        
        # Rotate the leaf
        rotated_leaf = pygame.transform.rotate(leaf_surface, angle)
        
        # Blit the leaf onto the tree
        self.image.blit(rotated_leaf, 
                       (x - rotated_leaf.get_width()//2, 
                        y - rotated_leaf.get_height()//2))
    
    def update(self):
        """Animate the palm tree swaying in the wind"""
        self.time += 1
        # Gentle swaying motion
        sway_amount = math.sin((self.time + self.animation_offset) * 0.05) * 2
        
        # Create a new image with the swaying effect
        original_image = self.image.copy()
        new_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        
        # Apply a slight shear transformation for swaying
        for y in range(self.image.get_height()):
            # More sway at the top, less at the bottom
            sway_factor = sway_amount * (1 - y / self.image.get_height())
            offset_x = int(sway_factor)
            
            # Copy each row with the calculated offset
            if 0 <= y < self.image.get_height():
                for x in range(self.image.get_width()):
                    new_x = x + offset_x
                    if 0 <= new_x < self.image.get_width():
                        new_image.set_at((new_x, y), original_image.get_at((x, y)))
        
        self.image = new_image 