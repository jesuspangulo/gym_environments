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
        self.low = np.array([0.0, 0.0, 0.0, 0, 0, 0, 0], dtype=np.float32)
        self.high = np.array([np.inf, np.inf, np.inf, 1, 1, 1, 1], dtype=np.float32)
        self.observation_space = spaces.Discrete(1)
        self.action_space = spaces.Discrete(4)
        self.current_state = self.game.get_state()
        self.current_action = 0
        self.current_reward = 0.0
        self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32)

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

        return np.array(self.current_state, dtype=np.float32), {}

    def step(self, action):
        self.current_action = action
        self.current_state = self.game.update(action)
        
        self.render()

        terminated = False
        return np.array(self.current_state, dtype=np.float32), self.current_reward, terminated, False, {}

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
