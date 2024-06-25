from settings import *

class Player(pygame.sprite.Sprite):
    
    def __init__(self, groups,pos) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(join('images','player','down','0.png'))
        self.rect = self.image.get_frect(center=pos)
        
        
        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 500
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self,dt):
       self.rect.center += self.direction * self.speed * dt
        
        
    def update(self, dt) -> None:
        self.input()
        self.move(dt)
        
        return super().update()
    
class AnimatedWalk(pygame.sprite.Sprite):
    def __init__(self, frames,pos,groups) -> None:
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0 
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
        
    def update(self,dt ) -> None:
        
        return super().update()
