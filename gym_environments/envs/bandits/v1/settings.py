import os

import pygame

ASSETS_DIR = os.path.join('.', 'assets')

TEXTURES = {
    'machine': pygame.image.load(os.path.join(ASSETS_DIR, "graphics", "slot-machine.png")),
    'arrow': pygame.image.load(os.path.join(ASSETS_DIR, "graphics", "up_arrow.png"))
}

pygame.font.init()

FONTS = {
    'large': pygame.font.Font(os.path.join(ASSETS_DIR, "fonts", "font.ttf"), 64)
}

MACHINE_WIDTH, MACHINE_HEIGHT = TEXTURES['machine'].get_size()

WINDOW_WIDTH = 150 + MACHINE_WIDTH * 2
WINDOWS_HEIGHT = 200 + MACHINE_HEIGHT
