from . import settings
from .Map import Map
from .Character import Character

class Scene:
    def __init__(self):
        self.map = None
        self.character_1 = None
        self.character_2 = None
        self.goal_x = 0
        self.goal_y = 0
        self.__load_environment()


    def __load_environment(self):
        with open(settings.CHARMAP, "r") as f:
            rows, cols = f.readline().split("x")
            rows, cols = int(rows), int(cols)
            self.map = Map(rows, cols)

            for i in range(rows):
                row = f.readline()
                for j in range(cols):
                    self.map.charmap[i][j] = row[j]
                    

            row, col = f.readline().split(",")
            row, col = int(row), int(col)
            self.goal_x, self.goal_y = col * settings.TILE_SIZE, row * settings.TILE_SIZE

            row, col = f.readline().split(",")
            row, col = int(row), int(col)
            x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE
            self.character_1 = Character(x, y, "pink", self.map)

            row, col = f.readline().split(",")
            row, col = int(row), int(col)
            x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE
            self.character_2 = Character(x, y, "blue", self.map)


    def reset(self):
        return self.get_state()

    def get_state(self):
        return []

    def check_win(self):
        return False
    
    def check_lose(self):
        return False
    
    def apply_action(self, action):
        self.character_1.apply_action(action)
        self.character_2.apply_action(action + 2)
    
    def render(self, surface):
        self.map.render(surface)
        surface.blit(settings.TEXTURES["yellow"], (self.goal_x, self.goal_y))
        self.character_1.render(surface)
        self.character_2.render(surface)


