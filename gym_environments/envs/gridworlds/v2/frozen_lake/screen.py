import pygame

from . import settings
from .tilemap import TileMap


class Screen:
    def __init__(self, title, num_tiles, P, state, action):
        pygame.init()
        pygame.display.init()
        self.render_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOWS_HEIGHT))
        pygame.display.set_caption(title)
        self.state = state
        self.action = action
        self.render_character = True
        self.tilemap = None
        self.finish_state = None
        self._create_tilemap(num_tiles, P)

    def _create_tilemap(self, num_tiles, P):
        tile_texture_names = {}
        for _, v in P.items():
            for _, v1 in v.items():
                for _, state, reward, terminated in v1:
                    if terminated:
                        if reward > 0:
                            self.finish_state = state
                        else:
                            tile_texture_names[state] = "hole"
                    else:
                        tile_texture_names[state] = "ice"
        tile_texture_names[self.finish_state] = "ice"
        self.tilemap = TileMap(num_tiles, tile_texture_names)

    def reset(self, state, action):
        self.state = state
        self.action = action
        self.tilemap.tiles[self.finish_state].texture_name = "ice"

    def update(self, state, action, reward, terminated):
        if terminated and reward == 0.0 and state != self.finish_state:
            self.tilemap.tiles[state].texture_name = "cracked_hole"
            self.render_character = False

        self.state = state
        self.action = action

    def render(self):
        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        self.render_surface.blit(
            settings.TEXTURES['cookie'],
            (self.tilemap.tiles[self.finish_state].x,
             self.tilemap.tiles[self.finish_state].y)
        )

        if self.render_character:
            self.render_surface.blit(
                settings.TEXTURES['character'][self.action],
                (self.tilemap.tiles[self.state].x,
                 self.tilemap.tiles[self.state].y)
            )

        self.screen.blit(
            pygame.transform.scale(
                self.render_surface,
                self.screen.get_size()),
            (0, 0)
        )
        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.display.quit()
        pygame.quit()
