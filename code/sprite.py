
from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True
        
        
            
class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        
class InvisibleCollision(pygame.sprite.Sprite):
    def __init__(self,pos,size, groups) -> None:
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_frect(topleft=pos)