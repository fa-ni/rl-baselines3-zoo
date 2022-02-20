import gym
import pytest

from src.main.rl.utils.utils import get_real_value, is_done, parse_scenario_name, delete_env_id
from src.main.services.ReactorCreatorService import ReactorCreatorService


@pytest.mark.parametrize(
    ["max_value", "scaled_value", "expected"],
    [[2000, -1, 0], [2000, 0.05, 1050], [2000, 0.95, 1950], [100, 1, 100], [100, 0, 50], [250, 0, 125]],
)
def test_get_real_value(max_value: int, scaled_value: float, expected: int):
    actual = get_real_value(max_value, scaled_value)
    print(actual)
    assert actual == expected


def test_is_done_true_because_of_failure():
    length = 200
    expected = True
    reactor = ReactorCreatorService.create_standard_full_reactor()
    reactor.reactor.blown()
    actual = is_done(reactor, length)
    assert actual == expected

    reactor = ReactorCreatorService.create_standard_full_reactor()
    reactor.generator.blown()
    actual = is_done(reactor, length)
    assert actual == expected

    reactor = ReactorCreatorService.create_standard_full_reactor()
    reactor.condenser.blown()
    actual = is_done(reactor, length)
    assert actual == expected

    reactor = ReactorCreatorService.create_standard_full_reactor()
    reactor.condenser_pump.blown()
    actual = is_done(reactor, length)
    assert actual == expected

    reactor = ReactorCreatorService.create_standard_full_reactor()
    reactor.condenser_pump.blown()
    reactor.condenser.blown()
    actual = is_done(reactor, 0)
    assert actual == expected

    reactor = ReactorCreatorService.create_standard_full_reactor()
    reactor.generator.blown()
    reactor.reactor.blown()
    reactor.condenser_pump.blown()
    actual = is_done(reactor, length)
    assert actual == expected


def test_is_done_true_because_of_length():
    reactor = ReactorCreatorService.create_standard_full_reactor()
    actual = is_done(reactor, 0)
    assert actual == True


def test_is_done_false():
    reactor = ReactorCreatorService.create_standard_full_reactor()
    actual = is_done(reactor, 200)
    assert actual == False


@pytest.mark.parametrize(
    ["scenario_name", "expected"],
    [
        ["scenario1", "scenario1"],
        ["scenario2Test", "scenario2"],
        ["Testscenario3Test", "scenario3"],
        ["Testscenario3Testscenario2", "scenario2"],
    ],
)
def test_parse_scenario_name(scenario_name: str, expected: str):
    actual = parse_scenario_name(scenario_name)
    assert actual == expected


def test_parse_scenario_name_throws_exception():
    with pytest.raises(Exception):
        parse_scenario_name("no_scenario_in_name")


def test_delete_env_id():
    env_id = "TestEnv-v1"
    gym.register(env_id)
    delete_env_id(env_id)
    env_dict = gym.envs.registration.registry.env_specs.copy()
    for env in env_dict:
        if env_id in env:
            assert False
