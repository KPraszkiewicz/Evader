from gymnasium.envs.registration import register

register(
    id='EvaderEnv-v1',
    entry_point='evader.envs:EvaderEnv_v1',
)