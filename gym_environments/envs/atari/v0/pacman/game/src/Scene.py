from .. import settings
from .Dot import Dot
from .Map import Map
from .entity.BaseEntity import Direction
from .entity.Ghost import Ghost
from .entity.Pacman import Pacman
from .search.Pathfinder import PathFinder
from .definitions.dots import DOTS


def distance(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def distance_v(v1, v2):
    return distance(v1.x, v2.x, v1.y, v2.y)


class Scene:
    def __init__(self):
        self.map = None
        self.pacman = None
        self.ghosts = []
        self.dots = []
        self.__load_environment()
        self.pathfinder = PathFinder(self.map)
        self.lose = False
  
    def __load_environment(self):
        with open(settings.CHARMAP, "r") as f:
            rows, cols = f.readline().split("x")
            rows, cols = int(rows), int(cols)
            self.map = Map(rows, cols)

            for i in range(rows):
                row = f.readline()
                for j in range(cols):
                    s = row[j]
                    if s in ('.', '*'):
                        x, y = j * settings.TILE_SIZE + settings.TILE_SIZE // 2, i * settings.TILE_SIZE + settings.TILE_SIZE // 2
                        defs = DOTS[s]
                        self.dots.append(Dot(x, y, defs))
                    else:
                        self.map.charmap[i][j] = s
                    

            row, col, speed, interval = f.readline().split(",")
            row, col, speed, interval = int(row), int(col), float(speed), float(interval)
            x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE
            self.pacman = Pacman(x, y, settings.TILE_SIZE, settings.TILE_SIZE, speed, settings.TEXTURES['pacman'], settings.FRAMES['pacman'], interval, self)
            """
            num_ghosts = int(f.readline())

            for _ in range(num_ghosts):
                row, col, color, speed, interval, mode = f.readline().split(",")
                row, col, color, speed, interval = int(row), int(col), int(color), float(speed), float(interval)
                x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE
                if mode[-1] == '\n':
                    mode = mode[:-1]
                self.ghosts.append(
                    Ghost(x, y, settings.TILE_SIZE, settings.TILE_SIZE, speed, settings.TEXTURES['ghosts'], settings.FRAMES['ghosts'][color], interval, self, mode)
                )
            """


    def reset(self):
        self.map = None
        self.pacman = None
        self.ghosts = []
        self.dots = []
        self.__load_environment()
        self.pathfinder = PathFinder(self.map)
        return self.get_state()

    def get_state(self):
        #dg1 = distance_v(self.pacman.position, self.ghosts[0].position)
        #dg2 = distance_v(self.pacman.position, self.ghosts[1].position)
        xp, yp = self.pacman.position.x, self.pacman.position.y

        if len(self.dots) == 0:
            min_dot = self.dots[0] 
            min_xd, min_yd = min_dot.position.x, min_dot.position.y
            min_dot_dist = distance(xp, min_xd, yp, min_yd)
            
            for dot in self.dots[1:]:
                dist = distance(xp, dot.position.x, yp, dot.position.y)
                if dist < min_dot_dist:
                    min_dot_dist = dist
                    min_xd = dot.position.x
                    min_yd = dot.position.y
        else:
            min_dot_dist = 0
            min_xd = xp
            min_yd = yp

        max_dist = distance(0, 10, 0, 10) * settings.TILE_SIZE

        pacman_dir = self.pacman.dir_to_num()

        pacman_moving_left = 1 if pacman_dir == Direction.LEFT else 0
        pacman_moving_down = 1 if pacman_dir == Direction.DOWN else 0
        pacman_moving_right = 1 if pacman_dir == Direction.RIGHT else 0
        pacman_moving_up = 1 if pacman_dir == Direction.UP else 0

        dot_to_left = 1 if min_xd < xp else 0
        dot_to_down = 1 if min_yd > yp else 0
        dot_to_right = 1 if min_xd > xp else 0
        dot_to_up = 1 if min_yd < yp else 0

        x = self.pacman.position.x / 160
        y = self.pacman.position.y / 160

        #return [x, y, dg1/max_dist, dg2/max_dist, dcd/max_dist, pacman_moving_left, pacman_moving_down, pacman_moving_right, pacman_moving_up]
        return [x, y, min_dot_dist/max_dist, pacman_moving_left, pacman_moving_down, pacman_moving_right, pacman_moving_up, dot_to_left, dot_to_down, dot_to_right, dot_to_up]

    def check_win(self):
        return len(self.dots) == 0
    
    def check_lose(self):
        return self.lose
    
    def apply_action(self, action):
        return self.pacman.apply_action(action)
    
    def update(self, dt):
        self.pacman.update(dt)

        for dot in self.dots:
            if self.pacman.get_collision_rect().colliderect(dot.get_collision_rect()):
                dot.eaten = True
                dot.on_collide(self.pacman)
        
        self.dots = [d for d in self.dots if not d.eaten]

        for ghost in self.ghosts:
            ghost.update(dt)

            if self.pacman.get_collision_rect().colliderect(ghost.get_collision_rect()):
                self.lose = True
    
    def render(self, surface):
        self.map.render(surface)
        for dot in self.dots:
            dot.render(surface)
        self.pacman.render(surface)
        for ghost in self.ghosts:
            ghost.render(surface)

        # To debug
        # self.pathfinder.render(surface, settings.TILE_SIZE)
