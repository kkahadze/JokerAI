from src.env import JokerEnv

# The following tests the proper sampling of an observation space
def test_observation_space_sample():
    env = JokerEnv()
    sample = env.observation_space.sample()
    in_play = sample["in_play"]
    assert int(in_play[0]) >= 0 and int(in_play[0]) <= 36
