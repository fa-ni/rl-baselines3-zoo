from src.main.rl.training import train_all_scenarios
from src.main.rl.utils.constants import ALL_SCENARIOS

if __name__ == "__main__":
    for _ in range(5):
        train_all_scenarios(ALL_SCENARIOS, "test_reward_2")
