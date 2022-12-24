from src.env import JokerEnv

# The following tests the proper sampling of an observation space
def test_observation_space_sample():
    env = JokerEnv()
    assert env.observation_space.sample()["in_play"][0]
