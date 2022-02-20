import numpy as np
from gym.spaces import Box, MultiBinary

from src.main.rl.envs.scenario2 import Scenario2


def test_scenario2_reset():
    scenario = Scenario2()
    actual = scenario.reset()
    assert actual == np.array([-1])


def test_scenario2_init():
    scenario = Scenario2()
    assert scenario.action_space == MultiBinary(n=2)
    assert scenario.observation_space == Box(np.array([-1]).astype(np.float32), np.array([1]).astype(np.float32))


def test_scenario2_step_with_two_actions():
    scenario = Scenario2()
    scenario.reset()
    step_one_result = scenario.step([1, 1])
    assert scenario.length == 249
    assert scenario.state.full_reactor.condenser_pump.rpm == 1600
    assert scenario.state.full_reactor.steam_valve1.status == True
    assert scenario.state.full_reactor.water_valve1.status == True
    assert scenario.state.full_reactor.condenser_pump.rpm_to_be_set == 1600
    assert scenario.state.full_reactor.reactor.moderator_percent == 99
    assert scenario.state.full_reactor.water_pump1.rpm_to_be_set == 25
    assert step_one_result == [np.array([-1.0]), 0.0, False, {}]
    step_two_result = scenario.step([0, 1])
    assert scenario.length == 248
    assert scenario.state.full_reactor.condenser_pump.rpm == 1600
    assert scenario.state.full_reactor.steam_valve1.status == True
    assert scenario.state.full_reactor.water_valve1.status == True
    assert scenario.state.full_reactor.condenser_pump.rpm_to_be_set == 1600
    assert scenario.state.full_reactor.reactor.moderator_percent == 100
    assert scenario.state.full_reactor.water_pump1.rpm_to_be_set == 50
    assert step_two_result == [np.array([-0.9975]), 0.0014285714285714286, False, {}]


def test_scenario2_step_with_three_actions():
    scenario = Scenario2()
    scenario.reset()
    step_one_result = scenario.step([1, 1, 0])
    assert scenario.length == 249
    assert scenario.state.full_reactor.condenser_pump.rpm == 1600
    assert scenario.state.full_reactor.steam_valve1.status == True
    assert scenario.state.full_reactor.water_valve1.status == False
    assert scenario.state.full_reactor.condenser_pump.rpm_to_be_set == 1600
    assert scenario.state.full_reactor.reactor.moderator_percent == 99
    assert scenario.state.full_reactor.water_pump1.rpm_to_be_set == 25
    assert step_one_result == [np.array([-1.0]), 0.0, False, {}]
    step_two_result = scenario.step([0, 1, 1])
    assert scenario.length == 248
    assert scenario.state.full_reactor.condenser_pump.rpm == 1600
    assert scenario.state.full_reactor.steam_valve1.status == True
    assert scenario.state.full_reactor.water_valve1.status == True
    assert scenario.state.full_reactor.condenser_pump.rpm_to_be_set == 1600
    assert scenario.state.full_reactor.reactor.moderator_percent == 100
    assert scenario.state.full_reactor.water_pump1.rpm_to_be_set == 50
    assert step_two_result == [np.array([-0.9975]), 0.0014285714285714286, False, {}]


def test_scenario2_step_with_five_actions():
    scenario = Scenario2()
    scenario.reset()
    step_one_result = scenario.step([1, 1, 0, 0, 1])
    assert scenario.length == 249
    assert scenario.state.full_reactor.steam_valve1.status == False
    assert scenario.state.full_reactor.water_valve1.status == False
    assert scenario.state.full_reactor.condenser_pump.rpm_to_be_set == 25
    assert scenario.state.full_reactor.reactor.moderator_percent == 99
    assert scenario.state.full_reactor.water_pump1.rpm_to_be_set == 25
    assert step_one_result == [np.array([-1.0]), 0.0, False, {}]
    step_two_result = scenario.step([0, 1, 1, 1, 0])
    assert scenario.length == 248
    assert scenario.state.full_reactor.steam_valve1.status == True
    assert scenario.state.full_reactor.water_valve1.status == True
    assert scenario.state.full_reactor.condenser_pump.rpm_to_be_set == 0
    assert scenario.state.full_reactor.reactor.moderator_percent == 100
    assert scenario.state.full_reactor.water_pump1.rpm_to_be_set == 50
    assert step_two_result == [np.array([-0.9975]), 0.0014285714285714286, False, {}]
