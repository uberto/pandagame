import pygame
import sys
import os
from enum import Enum
import math
import random

from panda_game.components.player import Player
from panda_game.levels.level import Level

# Game states
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETE = 4
    GAME_OVER = 5

class Game:
    def __init__(self):
        """Initialize the game"""
        # Debug mode
        self.DEBUG = False
        
        # Initialize pygame
        pygame.init()
        
        # Set up the display
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Panda Escape Adventure")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Game state
        self.state = GameState.MENU
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.SKY_BLUE = (135, 206, 235)
        self.OCEAN_BLUE = (65, 105, 225)  # Royal blue
        self.DEEP_BLUE = (0, 0, 139)      # Dark blue
        
        # Game title
        self.GAME_TITLE = "Panda Escape Adventure"
        
        # Set up the display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)
        
        # Create the player
        self.player = Player(50, 300)
        
        # Create the level
        self.current_level = 1
        self.level = Level(self.player, self.current_level)
        
        # Set player level boundaries
        self.player.set_level_boundaries(0, self.level.level_width)
        
        # Camera position (for scrolling)
        self.camera_x = 0
        self.camera_y = 0
        
        # Score and lives
        self.score = 0
        self.lives = 3
        
        # Font for text
        self.font = pygame.font.SysFont(None, 36)
        
        # Ocean animation variables
        self.wave_time = 0
        self.ocean_colors = [
            (65, 105, 225),  # Royal blue
            (70, 130, 230),  # Slightly lighter blue
            (75, 145, 235),  # Even lighter blue
            (70, 130, 230),  # Back to middle blue
        ]
        self.current_ocean_color_index = 0
        self.wave_speed = 0.05
        self.fish_positions = []
        self.seaweed_positions = []
        self.setup_ocean_decorations()
        
        # Print debug info if enabled
        if self.DEBUG:
            print(f"Game initialized with: Width={self.WINDOW_WIDTH}, Height={self.WINDOW_HEIGHT}, FPS={self.FPS}")
        
    def setup_ocean_decorations(self):
        """Set up decorative elements for the ocean"""
        # Create some fish at random positions
        for _ in range(10):
            x = random.randint(-200, -50)  # Start off-screen to the left
            y = random.randint(self.WINDOW_HEIGHT - 150, self.WINDOW_HEIGHT - 20)
            speed = random.uniform(0.5, 2.0)
            size = random.randint(5, 15)
            color = random.choice([
                (255, 165, 0),  # Orange
                (255, 215, 0),  # Gold
                (255, 69, 0),   # Red-Orange
                (135, 206, 250)  # Light Sky Blue
            ])
            self.fish_positions.append({
                'x': x, 'y': y, 'speed': speed, 'size': size, 
                'color': color, 'direction': 'right',
                'offset': random.randint(0, 100)
            })
        
        # Create some fish for the right side
        for _ in range(10):
            x = random.randint(self.WINDOW_WIDTH + 50, self.WINDOW_WIDTH + 200)  # Start off-screen to the right
            y = random.randint(self.WINDOW_HEIGHT - 150, self.WINDOW_HEIGHT - 20)
            speed = random.uniform(0.5, 2.0)
            size = random.randint(5, 15)
            color = random.choice([
                (255, 165, 0),  # Orange
                (255, 215, 0),  # Gold
                (255, 69, 0),   # Red-Orange
                (135, 206, 250)  # Light Sky Blue
            ])
            self.fish_positions.append({
                'x': x, 'y': y, 'speed': speed, 'size': size, 
                'color': color, 'direction': 'left',
                'offset': random.randint(0, 100)
            })
        
        # Create some seaweed
        for _ in range(8):
            x = random.randint(-150, -20)  # Left side
            y = self.WINDOW_HEIGHT
            height = random.randint(30, 80)
            width = random.randint(10, 20)
            segments = random.randint(3, 6)
            self.seaweed_positions.append({
                'x': x, 'y': y, 'height': height, 'width': width, 
                'segments': segments, 'offset': random.randint(0, 100)
            })
        
        for _ in range(8):
            x = random.randint(self.WINDOW_WIDTH + 20, self.WINDOW_WIDTH + 150)  # Right side
            y = self.WINDOW_HEIGHT
            height = random.randint(30, 80)
            width = random.randint(10, 20)
            segments = random.randint(3, 6)
            self.seaweed_positions.append({
                'x': x, 'y': y, 'height': height, 'width': width, 
                'segments': segments, 'offset': random.randint(0, 100)
            })
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.state == GameState.MENU:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = GameState.PLAYING
                    
            elif self.state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_p:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_UP:
                        self.player.climb(-1)  # Climb up
                    elif event.key == pygame.K_DOWN:
                        self.player.climb(1)   # Climb down
                
                # Handle key releases for climbing
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.player.stop_climbing()
                        
            elif self.state == GameState.PAUSED:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.state = GameState.PLAYING
                    
            elif self.state == GameState.LEVEL_COMPLETE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.current_level += 1
                    if self.current_level <= self.total_levels:
                        self.level = Level(self.current_level)
                        self.player.rect.x = 100
                        self.player.rect.y = self.WINDOW_HEIGHT - 100
                        self.state = GameState.PLAYING
                    else:
                        self.state = GameState.GAME_OVER
                        
            elif self.state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.current_level = 1
                    self.level = Level(self.current_level)
                    self.player.rect.x = 100
                    self.player.rect.y = self.WINDOW_HEIGHT - 100
                    self.state = GameState.MENU
                    
        # Handle continuous keyboard input for movement
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-1)
            elif keys[pygame.K_RIGHT]:
                self.player.move(1)
            else:
                self.player.velocity_x = 0
                
        return True
    
    def update(self):
        """Update game state"""
        if self.state == GameState.PLAYING:
            # Update the level
            self.level.update()
            
            # Update the player
            self.player.update(self.level.platform_list, self.level.bamboo_list)
            
            # Check for collisions with bamboo (collectibles)
            bamboo_collisions = pygame.sprite.spritecollide(self.player, self.level.bamboo_list, True)
            for bamboo in bamboo_collisions:
                self.score += 10
            
            # Check for collisions with animal cages
            cage_collisions = pygame.sprite.spritecollide(self.player, self.level.cage_list, False)
            for cage in cage_collisions:
                if not cage.is_open:
                    cage.open()
                    self.score += 50
            
            # Check for collisions with enemies
            enemy_collisions = pygame.sprite.spritecollide(self.player, self.level.enemy_list, False)
            if enemy_collisions:
                self.lives -= 1
                if self.lives <= 0:
                    self.state = GameState.GAME_OVER
                else:
                    # Reset player position
                    self.player.rect.x = 50
                    self.player.rect.y = 300
                    self.camera_x = 0
            
            # Check if level is complete (all cages opened)
            all_cages_open = True
            for cage in self.level.cage_list:
                if not cage.is_open:
                    all_cages_open = False
                    break
            
            if all_cages_open and len(self.level.cage_list) > 0:
                self.state = GameState.LEVEL_COMPLETE
            
            # Update camera position to follow player
            self.update_camera()
            
            # Update ocean animation
            self.wave_time += self.wave_speed
            if self.wave_time >= 1.0:
                self.wave_time = 0
                self.current_ocean_color_index = (self.current_ocean_color_index + 1) % len(self.ocean_colors)
            
            # Update fish positions
            for fish in self.fish_positions:
                if fish['direction'] == 'right':
                    fish['x'] += fish['speed']
                    if fish['x'] > self.WINDOW_WIDTH + 200:
                        fish['x'] = -50
                        fish['y'] = random.randint(self.WINDOW_HEIGHT - 150, self.WINDOW_HEIGHT - 20)
                else:  # 'left'
                    fish['x'] -= fish['speed']
                    if fish['x'] < -200:
                        fish['x'] = self.WINDOW_WIDTH + 50
                        fish['y'] = random.randint(self.WINDOW_HEIGHT - 150, self.WINDOW_HEIGHT - 20)
    
    def update_camera(self):
        """Update camera position to follow the player"""
        # Calculate target camera position (centered on player)
        target_x = self.player.rect.centerx - self.WINDOW_WIDTH // 2
        target_y = self.player.rect.centery - self.WINDOW_HEIGHT // 2
        
        # Smooth camera movement (lerp)
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # Clamp camera to level boundaries
        self.camera_x = max(0, min(self.camera_x, self.level.level_width - self.WINDOW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.level.level_height - self.WINDOW_HEIGHT))
        
        # Round camera position to avoid visual artifacts
        self.camera_x = round(self.camera_x)
        self.camera_y = round(self.camera_y)
    
    def draw(self):
        """Draw the game"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            # Draw the level
            self.level.draw(self.screen, int(self.camera_x))
            
            # Draw the player
            if self.player.facing_right:
                self.screen.blit(self.player.image, (self.player.rect.x - int(self.camera_x), self.player.rect.y))
            else:
                # Flip the player image if facing left
                flipped_image = pygame.transform.flip(self.player.image, True, False)
                self.screen.blit(flipped_image, (self.player.rect.x - int(self.camera_x), self.player.rect.y))
            
            # Draw the ocean
            self.draw_ocean()
            
            # Draw the HUD
            self.draw_hud()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.LEVEL_COMPLETE:
            self.draw_level_complete()
        
        # Update the display
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw the menu screen"""
        self.screen.fill(self.SKY_BLUE)
        
        # Draw title
        title = self.font.render(self.GAME_TITLE, True, self.BLACK)
        start_text = self.font.render("Press ENTER to Start", True, self.BLACK)
        controls_text = self.font.render("Controls: Arrow Keys, Space to Jump", True, self.BLACK)
        
        self.screen.blit(title, (self.WINDOW_WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(start_text, (self.WINDOW_WIDTH // 2 - start_text.get_width() // 2, 300))
        self.screen.blit(controls_text, (self.WINDOW_WIDTH // 2 - controls_text.get_width() // 2, 350))
    
    def draw_hud(self):
        """Draw the heads-up display"""
        # Draw level info
        level_text = self.font.render(f"Level: {self.current_level}", True, self.BLACK)
        self.screen.blit(level_text, (20, 20))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
        self.screen.blit(score_text, (20, 60))
        
        # Draw lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, self.BLACK)
        self.screen.blit(lives_text, (20, 100))
        
        # Draw debug info if enabled
        if self.DEBUG:
            climbing_text = self.font.render(f"Climbing: {self.player.climbing}", True, self.BLACK)
            position_text = self.font.render(f"Pos: ({self.player.rect.x}, {self.player.rect.y})", True, self.BLACK)
            camera_text = self.font.render(f"Camera: ({int(self.camera_x)}, {int(self.camera_y)})", True, self.BLACK)
            fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, self.BLACK)
            
            self.screen.blit(climbing_text, (20, 140))
            self.screen.blit(position_text, (20, 180))
            self.screen.blit(camera_text, (20, 220))
            self.screen.blit(fps_text, (self.WINDOW_WIDTH - 100, 20))
    
    def draw_game_over(self):
        """Draw the game over screen"""
        self.screen.fill(self.BLACK)
        
        # Draw game over text
        game_over_text = self.font.render("GAME OVER", True, self.WHITE)
        restart_text = self.font.render("Press ENTER to Restart", True, self.WHITE)
        
        self.screen.blit(game_over_text, (self.WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 250))
        self.screen.blit(restart_text, (self.WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 300))
    
    def draw_level_complete(self):
        """Draw the level complete screen"""
        self.screen.fill((0, 100, 0))  # Dark green background
        
        # Draw level complete text
        complete_text = self.font.render(f"LEVEL {self.current_level} COMPLETE!", True, self.WHITE)
        
        if self.current_level < 2:  # Assuming we have 2 levels for now
            next_text = self.font.render("Press ENTER for Next Level", True, self.WHITE)
        else:
            next_text = self.font.render("Press ENTER to Finish Game", True, self.WHITE)
        
        self.screen.blit(complete_text, (self.WINDOW_WIDTH // 2 - complete_text.get_width() // 2, 250))
        self.screen.blit(next_text, (self.WINDOW_WIDTH // 2 - next_text.get_width() // 2, 300))
    
    def draw_ocean(self):
        """Draw the ocean around the island"""
        # Get the current ocean color with interpolation for smooth transitions
        t = self.wave_time
        current_color = self.ocean_colors[self.current_ocean_color_index]
        next_color_index = (self.current_ocean_color_index + 1) % len(self.ocean_colors)
        next_color = self.ocean_colors[next_color_index]
        
        # Interpolate between current and next color
        r = int(current_color[0] * (1 - t) + next_color[0] * t)
        g = int(current_color[1] * (1 - t) + next_color[1] * t)
        b = int(current_color[2] * (1 - t) + next_color[2] * t)
        ocean_color = (r, g, b)
        
        # Draw left ocean (everything to the left of the level)
        if self.camera_x > 0:
            left_ocean_width = min(self.camera_x, self.WINDOW_WIDTH)
            left_ocean_rect = pygame.Rect(0, 0, left_ocean_width, self.WINDOW_HEIGHT)
            pygame.draw.rect(self.screen, ocean_color, left_ocean_rect)
            
            # Draw waves at the edge
            self.draw_waves(left_ocean_width, 0, self.WINDOW_HEIGHT, 'right')
            
            # Draw seaweed and fish in the left ocean
            self.draw_seaweed(0, left_ocean_width)
            self.draw_fish(0, left_ocean_width)
        
        # Draw right ocean (everything to the right of the level)
        right_edge_screen_x = self.level.level_width - self.camera_x
        if right_edge_screen_x < self.WINDOW_WIDTH:
            right_ocean_width = self.WINDOW_WIDTH - right_edge_screen_x
            right_ocean_rect = pygame.Rect(right_edge_screen_x, 0, right_ocean_width, self.WINDOW_HEIGHT)
            pygame.draw.rect(self.screen, ocean_color, right_ocean_rect)
            
            # Draw waves at the edge
            self.draw_waves(right_edge_screen_x, 0, self.WINDOW_HEIGHT, 'left')
            
            # Draw seaweed and fish in the right ocean
            self.draw_seaweed(right_edge_screen_x, self.WINDOW_WIDTH)
            self.draw_fish(right_edge_screen_x, self.WINDOW_WIDTH)
    
    def draw_waves(self, edge_x, top_y, height, direction):
        """Draw animated waves at the edge of the ocean"""
        wave_color = (255, 255, 255, 128)  # White with transparency for foam
        wave_height = 5
        wave_width = 10
        wave_count = height // 20
        
        for i in range(wave_count):
            y_pos = top_y + i * 20
            # Add some vertical movement based on time
            y_offset = math.sin(self.wave_time * 2 + i * 0.5) * 3
            y_pos += y_offset
            
            if direction == 'right':
                # Waves coming from left to right
                points = [
                    (edge_x - wave_width, y_pos),
                    (edge_x, y_pos - wave_height),
                    (edge_x + wave_width, y_pos)
                ]
            else:  # 'left'
                # Waves coming from right to left
                points = [
                    (edge_x, y_pos),
                    (edge_x - wave_width, y_pos - wave_height),
                    (edge_x - wave_width * 2, y_pos)
                ]
            
            pygame.draw.polygon(self.screen, wave_color, points)
    
    def draw_fish(self, left_bound, right_bound):
        """Draw fish in the ocean"""
        for fish in self.fish_positions:
            # Only draw fish within the visible ocean area
            if left_bound <= fish['x'] <= right_bound:
                # Fish body
                fish_x = fish['x']
                fish_y = fish['y'] + math.sin((self.wave_time * 3) + fish['offset']) * 5  # Wavy motion
                
                if fish['direction'] == 'right':
                    # Fish swimming right
                    pygame.draw.ellipse(self.screen, fish['color'], 
                                       [fish_x, fish_y, fish['size'] * 2, fish['size']])
                    # Tail
                    tail_points = [
                        (fish_x, fish_y + fish['size'] // 2),
                        (fish_x - fish['size'] // 2, fish_y),
                        (fish_x - fish['size'] // 2, fish_y + fish['size'])
                    ]
                    pygame.draw.polygon(self.screen, fish['color'], tail_points)
                    # Eye
                    pygame.draw.circle(self.screen, (0, 0, 0), 
                                      (int(fish_x + fish['size'] * 1.5), int(fish_y + fish['size'] // 3)), 
                                      max(1, fish['size'] // 4))
                else:
                    # Fish swimming left
                    pygame.draw.ellipse(self.screen, fish['color'], 
                                       [fish_x - fish['size'] * 2, fish_y, fish['size'] * 2, fish['size']])
                    # Tail
                    tail_points = [
                        (fish_x, fish_y + fish['size'] // 2),
                        (fish_x + fish['size'] // 2, fish_y),
                        (fish_x + fish['size'] // 2, fish_y + fish['size'])
                    ]
                    pygame.draw.polygon(self.screen, fish['color'], tail_points)
                    # Eye
                    pygame.draw.circle(self.screen, (0, 0, 0), 
                                      (int(fish_x - fish['size'] * 1.5), int(fish_y + fish['size'] // 3)), 
                                      max(1, fish['size'] // 4))
    
    def draw_seaweed(self, left_bound, right_bound):
        """Draw seaweed in the ocean"""
        for seaweed in self.seaweed_positions:
            # Only draw seaweed within the visible ocean area
            if left_bound <= seaweed['x'] <= right_bound:
                base_x = seaweed['x']
                base_y = seaweed['y']
                
                # Draw seaweed segments
                for i in range(seaweed['segments']):
                    segment_height = seaweed['height'] / seaweed['segments']
                    top_y = base_y - (i + 1) * segment_height
                    bottom_y = base_y - i * segment_height
                    
                    # Calculate x-offset for swaying motion
                    sway_amount = math.sin((self.wave_time * 2) + seaweed['offset'] + i * 0.5) * (i + 1) * 2
                    
                    # Seaweed colors
                    seaweed_color = (0, 100 + i * 20, 0)  # Darker at bottom, lighter at top
                    
                    # Draw a segment
                    points = [
                        (base_x + sway_amount - seaweed['width'] // 2, bottom_y),
                        (base_x + sway_amount + seaweed['width'] // 2, bottom_y),
                        (base_x + sway_amount * 1.5 + seaweed['width'] // 2, top_y),
                        (base_x + sway_amount * 1.5 - seaweed['width'] // 2, top_y)
                    ]
                    pygame.draw.polygon(self.screen, seaweed_color, points)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit() 