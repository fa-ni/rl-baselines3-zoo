import mock
import numpy as np
from src.main.rl.envs.scenario1 import Scenario1
from gym.spaces import Box


def test_scenario1_reset():
    scenario1 = Scenario1()
    actual = scenario1.reset()
    assert actual == np.array([-1])


def test_scenario1_init():
    scenario1 = Scenario1()
    assert scenario1.action_space == Box(np.array([-1, -1]).astype(np.float32), np.array([1, 1]).astype(np.float32))
    assert scenario1.observation_space == Box(np.array([-1]).astype(np.float32), np.array([1]).astype(np.float32))


@mock.patch("src.main.rl.envs.scenario1.get_real_value")
def test_scenario1_step_with_two_actions(mock_get_real_value):
    mock_get_real_value.return_value = 40
    scenario1 = Scenario1()
    scenario1.reset()
    step_one_result = scenario1.step([-1, 1])
    assert scenario1.length == 249
    assert scenario1.state.full_reactor.condenser_pump.rpm == 1600
    assert scenario1.state.full_reactor.steam_valve1.status == True
    assert scenario1.state.full_reactor.water_valve1.status == True
    assert scenario1.state.full_reactor.condenser_pump.rpm_to_be_set == 1600
    assert mock_get_real_value.call_count == 2
    assert scenario1.state.full_reactor.reactor.moderator_percent == 60
    assert scenario1.state.full_reactor.water_pump1.rpm_to_be_set == 40
    assert step_one_result == [np.array([-0.275]), 0.4142857142857143, False, {}]
    step_two_result = scenario1.step([-1, 1])
    assert scenario1.length == 248
    assert scenario1.state.full_reactor.condenser_pump.rpm == 1600
    assert scenario1.state.full_reactor.steam_valve1.status == True
    assert scenario1.state.full_reactor.water_valve1.status == True
    assert scenario1.state.full_reactor.condenser_pump.rpm_to_be_set == 1600
    assert mock_get_real_value.call_count == 4
    assert scenario1.state.full_reactor.reactor.moderator_percent == 20
    assert scenario1.state.full_reactor.water_pump1.rpm_to_be_set == 40
    assert step_two_result == [np.array([2.18]), 0, True, {}]


@mock.patch("src.main.rl.envs.scenario1.get_real_value")
def test_scenario1_step_with_three_actions(mock_get_real_value):
    mock_get_real_value.return_value = 40
    scenario1 = Scenario1()
    scenario1.reset()
    step_one_result = scenario1.step([-1, 1, -0.1])
    assert scenario1.length == 249
    assert scenario1.state.full_reactor.condenser_pump.rpm == 1600
    assert scenario1.state.full_reactor.steam_valve1.status == True
    assert scenario1.state.full_reactor.water_valve1.status == False
    assert scenario1.state.full_reactor.condenser_pump.rpm_to_be_set == 1600
    assert mock_get_real_value.call_count == 2
    assert scenario1.state.full_reactor.reactor.moderator_percent == 60
    assert scenario1.state.full_reactor.water_pump1.rpm_to_be_set == 40
    assert step_one_result == [np.array([-0.275]), 0.4142857142857143, False, {}]
    step_two_result = scenario1.step([-1, 1, 1])
    assert scenario1.length == 248
    assert scenario1.state.full_reactor.condenser_pump.rpm == 1600
    assert scenario1.state.full_reactor.steam_valve1.status == True
    assert scenario1.state.full_reactor.water_valve1.status == True
    assert scenario1.state.full_reactor.condenser_pump.rpm_to_be_set == 1600
    assert mock_get_real_value.call_count == 4
    assert scenario1.state.full_reactor.reactor.moderator_percent == 20
    assert scenario1.state.full_reactor.water_pump1.rpm_to_be_set == 40
    assert step_two_result == [np.array([2.18]), 0, True, {}]


@mock.patch("src.main.rl.envs.scenario1.get_real_value")
def test_scenario1_step_with_five_actions(mock_get_real_value):
    mock_get_real_value.return_value = 40
    scenario1 = Scenario1()
    scenario1.reset()
    step_one_result = scenario1.step([-1, 1, -0.5, -0.5, 0])
    assert scenario1.length == 249
    assert scenario1.state.full_reactor.steam_valve1.status == False
    assert scenario1.state.full_reactor.water_valve1.status == False
    assert scenario1.state.full_reactor.condenser_pump.rpm_to_be_set == 40
    assert mock_get_real_value.call_count == 3
    assert scenario1.state.full_reactor.reactor.moderator_percent == 60
    assert scenario1.state.full_reactor.water_pump1.rpm_to_be_set == 40
    assert step_one_result == [np.array([-1.0]), 0.0, False, {}]
    step_two_result = scenario1.step([-1, 1, 0.1, 0.3, 0])
    assert scenario1.length == 248
    assert scenario1.state.full_reactor.steam_valve1.status == True
    assert scenario1.state.full_reactor.water_valve1.status == True
    assert scenario1.state.full_reactor.condenser_pump.rpm_to_be_set == 40
    assert mock_get_real_value.call_count == 6
    assert scenario1.state.full_reactor.reactor.moderator_percent == 20
    assert scenario1.state.full_reactor.water_pump1.rpm_to_be_set == 40
    assert step_two_result == [np.array([2.18]), 0, True, {}]
