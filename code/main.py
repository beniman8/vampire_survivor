from typing import Any
from settings import *
from player import Player
from sprite import *
from random import randint,choice
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
        
        # sprites groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100
        
        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event,300)
        self.spawn_positions = []
        
        
        # setup
        self.load_images()
        self.setup()

        
        
        
    def load_images(self):
        self.bullet_surf =pygame.image.load(join('images','gun','bullet.png')).convert_alpha()
        
        folders = list(walk(join('images','enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images','enemies',folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names,key= lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path,file_name)
                    enemy_surf =pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(enemy_surf)
        
            
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
            else:
                self.spawn_positions.append((obj.x,obj.y))
                
                
            
                        
            
    def run(self):


        # Game Loop 
        while self.running:
            # Delta Time 
            dt = self.clock.tick() / 1000
            
            
            
            # Event Loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions),choice(list(self.enemy_frames.values())),(self.all_sprites,self.enemy_sprites),self.player,self.collision_sprites)   
                    
            
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