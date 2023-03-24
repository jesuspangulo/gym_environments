from pathlib import Path

import pygame

MAP_WIDTH = 17
MAP_HEIGHT = 12
TILE_SIZE = 32
DT = 1.0 / 60.0  # Emulation 60 fps as a fixed value
CHARACTER_SPEED = 70 * DT

VIRTUAL_WIDTH = MAP_WIDTH * TILE_SIZE
VIRTUAL_HEIGHT = MAP_HEIGHT * TILE_SIZE
WINDOW_WIDTH = VIRTUAL_WIDTH * 2
WINDOW_HEIGHT = VIRTUAL_HEIGHT * 2

BASE_DIR = Path(__file__).parent

CHARMAP = BASE_DIR / "maps" / "level1.txt"

TEXTURES = {
    "blue": pygame.image.load(BASE_DIR / "graphics" / "blue.png"),
    "pink": pygame.image.load(BASE_DIR / "graphics" / "pink.png"),
    "yellow": pygame.image.load(BASE_DIR / "graphics" / "yellow.png"),
}
