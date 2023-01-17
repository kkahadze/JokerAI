from src.env import JokerEnv
from src.utils import card_to_int

# The following tests the proper sampling of an observation space
def test_observation_space_sample():
    env = JokerEnv()
    sample = env.observation_space.sample()
    in_play = sample["in_play"]
    assert int(in_play[0]) >= 0 and int(in_play[0]) <= 46

def test_whole_epoch():
    env = JokerEnv()
    obs = env.reset()
    done = False
    while not done:
        action = card_to_int(env.game.players[0].play(obs))
        obs, reward, done, info = env.step(action)
        # print(f"PLAY: {env.game.play}")
        # print(f"ROUND: {env.game.round}")
    
    assert done and env.game.done
