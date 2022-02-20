import numpy as np
import pytest
from gym import register, make
from gym.spaces import Box

from src.main.rl.utils.utils import delete_env_id
from src.main.rl.wrapper.obs_wrapper2 import ObservationOption2Wrapper


@pytest.fixture
def set_up(request):
    version = request.node.get_closest_marker("number").args[0]
    env_id = f"test-v{version}"
    delete_env_id(env_id)
    scenario = "src.main.rl.envs.scenario2:Scenario2"
    register(id=env_id, entry_point=scenario)
    env = make(env_id)
    wrapper = ObservationOption2Wrapper(env)
    return wrapper


# Note:
# Wrapper can only be tested in direct combination with the scenarios.
@pytest.mark.number(1)
def test_step(set_up):
    wrapper = set_up
    wrapper.reset()
    # Necessary to instantiate the state
    actual_step_one = wrapper.step(action=[0, 1])
    actual_step_two = wrapper.step(action=[1, 1])
    actual_step_three = wrapper.step(action=[1, 1])
    assert len(actual_step_one[0]) == 3
    assert len(actual_step_two[0]) == 3
    assert all(actual_step_one[0] == np.array([-1, -0.987, 1]))
    assert all(actual_step_two[0] == np.array([-1, -0.968, 0.98]))
    assert all(actual_step_three[0] == np.array([-0.995, -0.946, 0.96]))


@pytest.mark.number(2)
def test_reset(set_up):
    wrapper = set_up
    actual = wrapper.reset()
    assert all(actual == np.array([-1, -1, 1]))


@pytest.mark.number(3)
def test_obs_space(set_up):
    wrapper = set_up
    assert wrapper.observation_space == Box(
        np.array([-1, -1, -1]).astype(np.float32), np.array([1, 1, 1]).astype(np.float32)
    )
