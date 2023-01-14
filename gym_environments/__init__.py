from gym.envs.registration import register

register(
    id='TwoArmedBandit-v0',
    entry_point='gym_environments.envs:TwoArmedBanditEnvV0',
)

register(
    id='TwoArmedBandit-v1',
    entry_point='gym_environments.envs:TwoArmedBanditEnvV1',
)
