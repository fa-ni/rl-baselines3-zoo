from src.main.rl.wrapper.reward_calculations import calculate_roofed_reward, calculate_reward_for_corridor
import pytest


@pytest.mark.parametrize(
    ["input", "expected"],
    [[700, 1], [0, 0], [1400, 0.5], [600, 0.85714]],
)
def test_calculate_roofed_reward(input: float, expected: float):
    actual = calculate_roofed_reward(input)
    assert round(actual, 5) == expected


@pytest.mark.parametrize(
    ["lower", "upper", "perfect", "number", "expected"],
    [[1500, 2500, 2100, 1500, 0],
     [1500, 2500, 2100, 2100, 1],
     [1500, 2500, 2100, 2200, 0.75],
     [1500, 2500, 2100, 2000, 0.83333],
     [1500, 2500, 2100, 1400, -1],
     [0, 350, 175, 0, 0],
     [0, 350, 175, 175, 1],
     [0, 350, 175, 325, 0.14286],
     [0, 350, 175, 25, 0.14286],
     [0, 350, 175, 400, -1]
     ]
)
def test_calculate_reward_for_corridor(lower, upper, perfect, number, expected):
    actual = calculate_reward_for_corridor(lower, upper, perfect, number)
    assert round(actual, 5) == expected
