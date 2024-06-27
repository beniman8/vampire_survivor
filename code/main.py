from typing import Any
from settings import *
from player import Player
from sprite import *
from random import randint
class Game:
    
    def __init__(self,game_name:str,width:int,height:int,running:bool) -> None:
        # General Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((width,height))
        self.running = running
        pygame.display.set_caption(game_name)
        self.clock = pygame.time.Clock()
        
        # sprites groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        # sprites
        self.player = Player((WINDOW_WIDTH/2,WINDOW_HEIGHT/2),self.all_sprites,self.collision_sprites)
        for i in range(6):
            x, y = randint(0,WINDOW_WIDTH), randint(0,WINDOW_HEIGHT)
            w, h = randint(60,100),randint(50,100)
            CollisionSprite(pos=(x,y),size=(w,h),groups=(self.all_sprites,self.collision_sprites))

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
            self.all_sprites.update(dt)
                    
            # Draw The Game
            self.display_surface.fill('#3a2e3f')
            self.all_sprites.draw(self.display_surface)
            
            # Update The Display
            pygame.display.update()
    
        pygame.quit()




if __name__ == '__main__':
    # Run The Game      
    game=Game('Vampire Survivor',WINDOW_WIDTH,WINDOW_HEIGHT,True)
    game.run()