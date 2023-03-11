import time

import numpy as np

import pygame

import gym
from gym import spaces

from .game.Game import Game


class PacmanEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, **kwargs):
        super().__init__()
        self.render_mode = kwargs.get("render_mode")
        self.game = Game("Pacman Atari Env", self.render_mode)
        self.observation_space = spaces.Discrete(1)
        self.action_space = spaces.Discrete(5)
        self.current_state = self.game.get_state()
        self.current_action = 0
        self.current_reward = 0.0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get("delay", 0.5)

        np.random.seed(seed)

        self.current_state = self.game.reset()
        self.current_action = 0
        self.current_reward = 0

        return 0, {}

    def step(self, action):
        _, win, lose = self.game.update(action, self.metadata['render_fps'])
        self.game.render()
        terminated = win or lose
        return 0, 0.0, terminated, False, {}

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
