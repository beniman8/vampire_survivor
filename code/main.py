from typing import Any
from settings import *
from player import Player
from sprite import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites



class Game:
    
    def __init__(self,game_name:str,width:int,height:int,running:bool) -> None:
        # General Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((width,height))
        self.running = running
        pygame.display.set_caption(game_name)
        self.clock = pygame.time.Clock()
        self.load_images()
        
        # sprites groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.setup()
        
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100
        # sprites
        


    def load_images(self):
        self.bullet_surf =pygame.image.load(join('images','gun','bullet.png')).convert_alpha()
            
    def input(self):
        recent_keys = pygame.mouse.get_just_pressed()
        if recent_keys[2] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf,pos,self.gun.player_direction,(self.all_sprites,self.bullet_sprites))
            
            self.can_shoot = False 
            self.shoot_time = pygame.time.get_ticks()
            
    def gun_timer(self):
        if not self.can_shoot:
            current_Time = pygame.time.get_ticks()
            if current_Time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
                
    def setup(self):
        map = load_pygame(join('data','maps','world.tmx'))

            
        for x, y , image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE),image,(self.all_sprites))
            
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))
            
        for col in map.get_layer_by_name('Collisions'):
            InvisibleCollision((col.x,col.y),(col.width,col.height),(self.collision_sprites))
            
            
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y),self.all_sprites,self.collision_sprites)
                self.gun = Gun(self.player,self.all_sprites)
                
                
            
            
            
    def run(self):


        # Game Loop 
        while self.running:
            # Delta Time 
            dt = self.clock.tick() / 1000
            
            
            # Event Loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            
            # Update The Game
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
                    
            # Draw The Game
            self.display_surface.fill('#3a2e3f')
            self.all_sprites.draw(self.player.rect.center)
            
            # Update The Display
            pygame.display.update()
    
        pygame.quit()




if __name__ == '__main__':
    # Run The Game      
    game=Game('Vampire Survivor',WINDOW_WIDTH,WINDOW_HEIGHT,True)
    game.run()