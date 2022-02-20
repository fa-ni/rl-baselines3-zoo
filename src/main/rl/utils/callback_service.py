import os

import numpy as np
from gym.wrappers.monitor import load_results
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.results_plotter import ts2xy


class SaveOnBestTrainingRewardCallback(BaseCallback):
    def __init__(
        self, check_freq, log_dir, minimum_required_reward: int = 190, number_of_last_episodes_to_check: int = 100
    ):
        super(SaveOnBestTrainingRewardCallback, self).__init__()
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, "best_model")
        self.best_mean_reward = -np.inf
        self.minimum_required_reward = minimum_required_reward
        self.number_of_last_episodes_to_check = number_of_last_episodes_to_check

    def _init_callback(self) -> None:
        # Create folder if needed
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            # Retrieve training reward
            x, y = ts2xy(load_results(self.log_dir), "timesteps")
            if len(x) > 0:
                # Mean training reward over the last 100 episodes
                mean_reward = np.mean(y[-self.number_of_last_episodes_to_check :])
                # New best model, you could save the agent here
                if mean_reward > self.best_mean_reward and mean_reward > self.minimum_required_reward:
                    self.best_mean_reward = mean_reward
                    # Example for saving best model
                    self.model.save(self.save_path)
        return True
