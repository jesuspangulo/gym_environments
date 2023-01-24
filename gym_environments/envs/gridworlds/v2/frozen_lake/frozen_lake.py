import time

import numpy as np

import gym
from gym import spaces
import pygame

from . import settings
from .screen import Screen


class FrozenLakeEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.observation_space = spaces.Discrete(16)
        self.action_space = spaces.Discrete(4)
        self.current_action = 1
        self.current_state = 0
        self.current_reward = None
        self.delay = settings.DEFAULT_DELAY
        self.P = settings.P
        self.screen = Screen(
            "Frozen Lake Environment",
            self.observation_space.n,
            self.P,
            self.current_state,
            self.current_action)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.5)

        np.random.seed(seed)
        self.current_state = 0
        self.screen.reset()
        return 0, {}

    def step(self, action):
        self.current_action = action

        posibilities = self.P[self.current_state][self.current_action]

        p = 0
        i = 0

        r = np.random.random()
        while r > p:
            r -= p
            p, self.current_state, self.current_reward, terminated = posibilities[i]
            i += 1

        self.screen.update(
            self.current_state,
            self.current_action,
            self.current_reward,
            terminated)
        self.render()
        time.sleep(self.delay)

        return self.current_state, self.current_reward, terminated, False, {}

    def render(self):
        self.screen.render()

    def close(self):
        self.screen.close()
