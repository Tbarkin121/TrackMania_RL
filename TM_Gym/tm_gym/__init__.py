from gym.envs.registration import register
register(
    id='TrackMania-v0',
    entry_point='tm_gym.envs:TrackManiaEnv'
)