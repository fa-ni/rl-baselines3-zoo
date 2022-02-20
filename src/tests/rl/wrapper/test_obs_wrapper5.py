import numpy as np
import pytest
from gym import register, make
from gym.spaces import Box

from src.main.rl.utils.utils import delete_env_id
from src.main.rl.wrapper.obs_wrapper5 import ObservationOption5Wrapper


@pytest.fixture
def set_up(request):
    version = request.node.get_closest_marker("number").args[0]
    env_id = f"test-v{version}"
    delete_env_id(env_id)
    scenario = "src.main.rl.envs.scenario2:Scenario2"
    register(id=env_id, entry_point=scenario)
    env = make(env_id)
    wrapper = ObservationOption5Wrapper(env)
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
    assert len(actual_step_one[0]) == 10
    assert len(actual_step_two[0]) == 10
    np.testing.assert_almost_equal(actual_step_one[0], np.array([-1, 0.0005, -1, -0.00025, -1, -0.987, 1, 0.6, 1, 1]))
    np.testing.assert_almost_equal(
        actual_step_two[0], np.array([-1, 0.0, -0.99868, -0.00036, -1, -0.968, 0.98, 0.6, 1, 1]), 5
    )
    np.testing.assert_almost_equal(
        actual_step_three[0], np.array([-0.995, -0.00089, -0.99611, -0.00064, -0.99980, -0.946, 0.96, 0.6, 1, 1]), 5
    )


@pytest.mark.number(2)
def test_reset(set_up):
    wrapper = set_up
    actual = wrapper.reset()
    np.testing.assert_almost_equal(actual, np.array([-1, 0, -1, 0, -1, -1, 1, 0.6, 1, 1]))


@pytest.mark.number(3)
def test_obs_space(set_up):
    wrapper = set_up
    assert wrapper.observation_space == Box(
        np.array([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]).astype(np.float32),
        np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).astype(np.float32),
    )
