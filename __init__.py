from gym.envs.registration import register

register(
    id='TwoArmedBandit-v0',
    entry_point='gym_envs.envs:TwoArmedBanditEnv',
)