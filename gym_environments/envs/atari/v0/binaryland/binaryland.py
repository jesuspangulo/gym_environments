import time

import numpy as np

import gym
from gym import spaces

from .game.Game import Game


class BinarylandEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, **kwargs):
        super().__init__()
        self.render_mode = kwargs.get("render_mode")
        self.game = Game("Pacman Atari Env", self.render_mode)
        self.low = np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float32)
        self.high = np.array([np.inf, np.inf, np.inf, np.inf], dtype=np.float32)
        self.observation_space = spaces.Discrete(1)
        self.action_space = spaces.Discrete(4)
        self.current_state = self.game.get_state()
        self.current_action = 0
        self.current_reward = 0.0
        self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32)
        self.action_counter = 0

    def __get_state(self):
        return np.array(self.current_state, dtype=np.float32)

    def __get_info(self):
        return self.game.get_info()

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
        self.action_counter = 0

        return self.__get_state(), self.__get_info()

    def step(self, action):
        self.action_counter += 1
        self.current_action = action
        self.current_state, terminated = self.game.update(action)
        truncated = False

        d1i, d1j, d2i, d2j = self.current_state

        di = max(d1i, d2i)
        dj = max(d1j, d2j)

        if di <= 0.000001:
            self.current_reward = -10 * dj
        else:
            self.current_reward = -50 * di

        if terminated:
            self.current_reward = 10000
        elif self.action_counter >= 50000:
            self.current_reward = -1000
            truncated = True

        self.render()
        return (
            self.__get_state(),
            self.current_reward,
            terminated,
            truncated,
            self.__get_info(),
        )

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
