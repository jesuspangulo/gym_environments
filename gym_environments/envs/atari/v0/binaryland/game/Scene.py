from . import settings
from .Map import Map
from .Entity import Entity
from .Character import Character


class Scene:
    def __init__(self):
        self.map = None
        self.character_1 = None
        self.character_2 = None
        self.goal = None
        self.__load_environment()

        self.mirror = [2, 1, 0, 3]

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
            x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE
            self.goal = Entity(x, y, "yellow")

            row, col = f.readline().split(",")
            row, col = int(row), int(col)
            x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE
            self.character_1 = Character(x, y, "pink", self.map)

            row, col = f.readline().split(",")
            row, col = int(row), int(col)
            x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE
            self.character_2 = Character(x, y, "blue", self.map)

    def __get_available_actions(self):
        return [
            action
            for action in range(4)
            if self.character_1.can_move(action)
            or self.character_2.can_move(self.mirror[action])
        ]

    def reset(self):
        self.map = None
        self.character_1 = None
        self.character_2 = None
        self.goal = None
        self.__load_environment()
        return self.get_state()

    def get_state(self):

        c1i, c1j = int(self.character_1.y // settings.TILE_SIZE), int(
            self.character_1.x // settings.TILE_SIZE
        )
        c2i, c2j = int(self.character_2.y // settings.TILE_SIZE), int(
            self.character_2.x // settings.TILE_SIZE
        )
        gi, gj = int(self.goal.y // settings.TILE_SIZE), int(
            self.goal.x // settings.TILE_SIZE
        )

        d1i = abs(c1i - gi)
        d1j = abs(c1j - gj)
        d2i = abs(c2i - gi)
        d2j = abs(c2j - gj)

        c1x, c1y = self.character_1.get_collision_rect().center
        c2x, c2y = self.character_2.get_collision_rect().center
        gx, gy = self.goal.get_collision_rect().center

        d1i = abs(c1y - gy)
        d1j = abs(c1x - gx)
        d2i = abs(c2y - gy)
        d2j = abs(c2x - gx)

        return [300 / d1i, 300 / d1j, 300 / d2i, 300 / d2j]

    def get_info(self):
        return {"available_actions": self.__get_available_actions()}

    def check_win(self):
        return self.character_1.collides_with(
            self.goal
        ) and self.character_2.collides_with(self.goal)

    def check_lose(self):
        return False

    def apply_action(self, action):
        self.character_1.apply_action(action)
        self.character_2.apply_action(self.mirror[action])

    def render(self, surface):
        self.map.render(surface)
        self.goal.render(surface)
        self.character_1.render(surface)
        self.character_2.render(surface)
