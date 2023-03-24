import pygame

from . import settings


class Entity:
    def __init__(self, x, y, texture_name):
        self.x = x
        self.y = y
        self.texture_name = texture_name
    
    def get_collision_rect(self):
        return pygame.Rect(self.x + 1, self.y + 1, settings.TILE_SIZE - 2, settings.TILE_SIZE - 2)
    
    def collides_with(self, another):
        return self.get_collision_rect().colliderect(another.get_collision_rect())
    
    def render(self, surface):
        surface.blit(settings.TEXTURES[self.texture_name], (self.x, self.y))
