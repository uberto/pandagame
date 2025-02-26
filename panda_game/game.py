import pygame
import sys
import os
from enum import Enum

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
        # Initialize Pygame
        pygame.init()
        
        # Load constants from environment variables
        self.WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', 800))
        self.WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', 600))
        self.FPS = int(os.getenv('FPS', 60))
        self.GAME_TITLE = os.getenv('GAME_TITLE', 'Panda Escape Adventure')
        self.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.SKY_BLUE = (135, 206, 235)
        
        # Set up the display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.MENU
        self.current_level = 1
        self.total_levels = 2  # For now, we have 2 levels
        
        # Create player
        self.player = Player(100, self.WINDOW_HEIGHT - 100)
        
        # Create level
        self.level = Level(self.current_level)
        
        # Font for text
        self.font = pygame.font.SysFont(None, 36)
        
        # Print debug info if enabled
        if self.DEBUG:
            print(f"Game initialized with: Width={self.WINDOW_WIDTH}, Height={self.WINDOW_HEIGHT}, FPS={self.FPS}")
        
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
        if self.state == GameState.PLAYING:
            # Update level
            self.level.update()
            
            # Update player with collision detection
            self.player.update(self.level.platforms, self.level.bamboo)
            
            # Check for cage collision (to free animals)
            cage_collisions = pygame.sprite.spritecollide(self.player, self.level.cages, False)
            for cage in cage_collisions:
                cage.open_cage()
                
            # Check if all cages are open
            all_open = True
            for cage in self.level.cages:
                if not cage.is_open:
                    all_open = False
                    break
                    
            if all_open:
                self.state = GameState.LEVEL_COMPLETE
                
            # Check for enemy collision (game over)
            enemy_collisions = pygame.sprite.spritecollide(self.player, self.level.enemies, False)
            if enemy_collisions:
                self.state = GameState.GAME_OVER
    
    def draw(self):
        self.screen.fill(self.SKY_BLUE)
        
        if self.state == GameState.MENU:
            # Draw menu
            title = self.font.render(self.GAME_TITLE, True, self.BLACK)
            start_text = self.font.render("Press ENTER to Start", True, self.BLACK)
            controls_text = self.font.render("Controls: Arrow Keys, Space to Jump", True, self.BLACK)
            
            self.screen.blit(title, (self.WINDOW_WIDTH // 2 - title.get_width() // 2, 200))
            self.screen.blit(start_text, (self.WINDOW_WIDTH // 2 - start_text.get_width() // 2, 300))
            self.screen.blit(controls_text, (self.WINDOW_WIDTH // 2 - controls_text.get_width() // 2, 350))
            
        elif self.state == GameState.PLAYING:
            # Draw level
            self.level.draw(self.screen)
            
            # Draw player
            self.screen.blit(self.player.image, self.player.rect)
            
            # Draw level info
            level_text = self.font.render(f"Level: {self.current_level}", True, self.BLACK)
            self.screen.blit(level_text, (20, 20))
            
            # Draw climbing status if in debug mode
            if self.DEBUG:
                climbing_text = self.font.render(f"Climbing: {self.player.climbing}", True, self.BLACK)
                self.screen.blit(climbing_text, (20, 60))
            
        elif self.state == GameState.PAUSED:
            # Draw paused screen
            paused_text = self.font.render("PAUSED", True, self.BLACK)
            continue_text = self.font.render("Press P to Continue", True, self.BLACK)
            
            self.screen.blit(paused_text, (self.WINDOW_WIDTH // 2 - paused_text.get_width() // 2, 250))
            self.screen.blit(continue_text, (self.WINDOW_WIDTH // 2 - continue_text.get_width() // 2, 300))
            
        elif self.state == GameState.LEVEL_COMPLETE:
            # Draw level complete screen
            complete_text = self.font.render(f"LEVEL {self.current_level} COMPLETE!", True, self.BLACK)
            next_text = self.font.render("Press ENTER for Next Level", True, self.BLACK)
            
            self.screen.blit(complete_text, (self.WINDOW_WIDTH // 2 - complete_text.get_width() // 2, 250))
            self.screen.blit(next_text, (self.WINDOW_WIDTH // 2 - next_text.get_width() // 2, 300))
            
        elif self.state == GameState.GAME_OVER:
            # Draw game over screen
            if self.current_level > self.total_levels:
                # Player won the game
                game_over_text = self.font.render("CONGRATULATIONS! YOU WON!", True, self.BLACK)
            else:
                # Player lost
                game_over_text = self.font.render("GAME OVER", True, self.BLACK)
                
            restart_text = self.font.render("Press ENTER to Restart", True, self.BLACK)
            
            self.screen.blit(game_over_text, (self.WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 250))
            self.screen.blit(restart_text, (self.WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 300))
        
        # Draw debug info if enabled
        if self.DEBUG:
            fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, self.BLACK)
            self.screen.blit(fps_text, (self.WINDOW_WIDTH - 100, 20))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit() 