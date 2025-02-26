import pygame
from panda_game.components.objects import Platform, Bamboo, AnimalCage, Enemy

class Level:
    def __init__(self, level_num=1):
        self.level_num = level_num
        self.platforms = pygame.sprite.Group()
        self.bamboo = pygame.sprite.Group()
        self.cages = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        
        # Set up the level
        self.setup_level()
        
    def setup_level(self):
        """Set up the level layout based on level number"""
        if self.level_num == 1:
            # Ground platform
            ground = Platform(0, 550, 800, 50)
            self.platforms.add(ground)
            self.all_sprites.add(ground)
            
            # Some platforms
            platform1 = Platform(100, 450, 200, 20)
            platform2 = Platform(400, 350, 200, 20)
            platform3 = Platform(200, 250, 200, 20)
            self.platforms.add(platform1, platform2, platform3)
            self.all_sprites.add(platform1, platform2, platform3)
            
            # Bamboo stalks
            bamboo1 = Bamboo(350, 250, 300)
            bamboo2 = Bamboo(650, 350, 200)
            self.bamboo.add(bamboo1, bamboo2)
            self.all_sprites.add(bamboo1, bamboo2)
            
            # Animal cage
            cage = AnimalCage(700, 500, "monkey")
            self.cages.add(cage)
            self.all_sprites.add(cage)
            
            # Enemy
            enemy = Enemy(400, 530, 300, 600)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            
        elif self.level_num == 2:
            # Different layout for level 2
            # Ground platform
            ground = Platform(0, 550, 800, 50)
            self.platforms.add(ground)
            self.all_sprites.add(ground)
            
            # Some platforms
            platform1 = Platform(50, 450, 150, 20)
            platform2 = Platform(300, 400, 150, 20)
            platform3 = Platform(550, 350, 150, 20)
            platform4 = Platform(300, 250, 150, 20)
            platform5 = Platform(50, 200, 150, 20)
            self.platforms.add(platform1, platform2, platform3, platform4, platform5)
            self.all_sprites.add(platform1, platform2, platform3, platform4, platform5)
            
            # Bamboo stalks
            bamboo1 = Bamboo(250, 200, 350)
            bamboo2 = Bamboo(500, 250, 300)
            bamboo3 = Bamboo(700, 350, 200)
            self.bamboo.add(bamboo1, bamboo2, bamboo3)
            self.all_sprites.add(bamboo1, bamboo2, bamboo3)
            
            # Animal cage
            cage = AnimalCage(100, 150, "tiger")
            self.cages.add(cage)
            self.all_sprites.add(cage)
            
            # Enemies
            enemy1 = Enemy(200, 530, 100, 400)
            enemy2 = Enemy(600, 530, 500, 700)
            self.enemies.add(enemy1, enemy2)
            self.all_sprites.add(enemy1, enemy2)
    
    def update(self):
        """Update all sprites in the level"""
        self.all_sprites.update()
        
    def draw(self, screen):
        """Draw all sprites to the screen"""
        self.all_sprites.draw(screen) 