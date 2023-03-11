import pygame

from .AbstractEntity import AbstractEntity


class Pacman(AbstractEntity):
    def __init__(self, x, y, w, h, speed, interval, texture, frames, scene):
        animations = {
            (-1, 0): frames[0],
            (0, 1): frames[1],
            (1, 0): frames[2],
            (0, -1): frames[3],
        }
        super().__init__(x, y, w, h, speed, interval, texture, animations)
        self.current_animation = [frames[0][0]]
        self.scene = scene
        self.buffer_direction = self.direction.copy()
        self.action_map = [self.request_left, self.request_down, self.request_right, self.request_up, self.do_nothing]
        self.score = 0
    
    def request_left(self):
        self.buffer_direction = pygame.Vector2(-1, 0)
    
    def request_down(self):
        self.buffer_direction = pygame.Vector2(0, 1)
    
    def request_right(self):
        self.buffer_direction = pygame.Vector2(1, 0)
    
    def request_up(self):
        self.buffer_direction = pygame.Vector2(0, -1)

    def do_nothing(self):
        pass

    def apply_action(self, action):
        self.action_map[action]()

    def handle_arrive(self):
        self.direction = pygame.Vector2(0, 0)
        i, j = int(self.position.y // self.size.y), int(self.position.x // self.size.x)
        if self.scene.map.charmap[i][j] in ('.', '*'):
            self.score += 1
        self.scene.map.charmap[i][j] = ''
        n_i, n_j = int(i + self.buffer_direction.y), int(j + self.buffer_direction.x)

        if self.scene.map.charmap[n_i][n_j] != '#':
            self.direction = self.buffer_direction.copy()
        self.target = self.source + self.direction * 32