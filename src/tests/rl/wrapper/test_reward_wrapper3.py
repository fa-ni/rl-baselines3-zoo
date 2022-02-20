from src.main.rl.utils.utils import delete_env_id
from src.main.rl.wrapper.reward_wrapper3 import RewardOption3Wrapper
import pytest
import mock
import gym
#@pytest.fixture
from src.main.services.ReactorCreatorService import ReactorCreatorService


def set_up():
    #version = request.node.get_closest_marker("number").args[0]
    env_id = f"test-v1"#{version}"
    delete_env_id(env_id)
    scenario = "src.main.rl.envs.scenario2:Scenario2"
    gym.register(id=env_id, entry_point=scenario)
    env = gym.make(env_id)
    env.reset()
    wrapper = RewardOption3Wrapper(env)
    return wrapper

@mock.patch("src.main.rl.wrapper.reward_wrapper3.calculate_roofed_reward")
@mock.patch("src.main.rl.wrapper.reward_wrapper3.calculate_reward_for_corridor")
@mock.patch("src.main.rl.wrapper.reward_wrapper3.is_done")
#@pytest.mark.number(1)
def test_reward_wrapper3(mock1,mock2,mock3):
    mock1.return_value= False
    mock2.side_effect= [1,0.5,0.2]
    mock3.side_effect= [0.4]
    wrapper = set_up()
    actual=wrapper.reward(0)
    expected=2
    assert mock1.call_count==1
    assert mock2.call_count==3
    assert mock3.call_count==1

    assert actual == expected