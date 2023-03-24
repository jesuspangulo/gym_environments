import pygame

from . import settings
from .Entity import Entity


class Character(Entity):
    def __init__(self, x, y, texture_name, map):
        super().__init__(x, y, texture_name)
        self.map = map
        self.actions_map = [
            self.move_left,
            self.move_down,
            self.move_right,
            self.move_up,
        ]

    def move_up(self):
        rect = self.get_collision_rect()

        next_y = self.y - settings.CHARACTER_SPEED
        i = int(next_y // settings.TILE_SIZE)
        l = int(rect.left // settings.TILE_SIZE)
        r = int(rect.right // settings.TILE_SIZE)

        if "#" in (self.map.charmap[i][l], self.map.charmap[i][r]):
            return False, None, None

        return True, self.x, next_y

    def move_down(self):
        rect = self.get_collision_rect()

        next_y = self.y + settings.CHARACTER_SPEED
        i = int((rect.bottom + 1) // settings.TILE_SIZE)
        l = int(rect.left // settings.TILE_SIZE)
        r = int(rect.right // settings.TILE_SIZE)

        if "#" in (self.map.charmap[i][l], self.map.charmap[i][r]):
            return False, None, None

        return True, self.x, next_y

    def move_left(self):
        rect = self.get_collision_rect()

        next_x = self.x - settings.CHARACTER_SPEED
        j = int(next_x // settings.TILE_SIZE)
        t = int(rect.top // settings.TILE_SIZE)
        b = int(rect.bottom // settings.TILE_SIZE)

        if "#" in (self.map.charmap[t][j], self.map.charmap[b][j]):
            return False, None, None

        return True, next_x, self.y

    def move_right(self):
        rect = self.get_collision_rect()

        next_x = self.x + settings.CHARACTER_SPEED
        j = int((rect.right + 1) // settings.TILE_SIZE)
        t = int(rect.top // settings.TILE_SIZE)
        b = int(rect.bottom // settings.TILE_SIZE)

        if "#" in (self.map.charmap[t][j], self.map.charmap[b][j]):
            return False, None, None

        return True, next_x, self.y

    def apply_action(self, action):
        moved, new_x, new_y = self.actions_map[action]()
        if moved:
            self.x = new_x
            self.y = new_y

    def can_move(self, action):
        moved, _, _ = self.actions_map[action]()
        return moved
