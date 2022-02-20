import gym
import mock

from src.main.rl.utils.constants import ALL_SCENARIOS
from src.main.rl.training import train_all_scenarios


@mock.patch("src.main.rl.training.train_agent")
def test_number_of_models_with_one_envs(mock_train_agent):
    scenarios = ["src.main.rl.envs.scenario2:Scenario2"]
    train_all_scenarios(scenarios)
    # Count is the following:
    # 2 (ActionWrapper) * 4 (ObservationWrappers) * 3 (Alg) = 24
    # 2 (ActionWrapper) without Obs * 3 (Alg) = 6
    # 4 (ObservationWrappers) without Action * 3 (Alg) = 12
    # 1 without Action and without Obs * 3 (Alg) = 3
    # 24+6+12+3=45
    assert mock_train_agent.call_count == 45
    # Resetting all registered envs in gym
    gym.envs.registration.registry.env_specs.clear()


@mock.patch("src.main.rl.training.train_agent")
def test_number_of_models_with_three_envs(mock_train_agent):
    train_all_scenarios(ALL_SCENARIOS)
    assert mock_train_agent.call_count == 45 * 3
