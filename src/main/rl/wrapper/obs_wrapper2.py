import numpy as np
from gym import Wrapper
from gym.spaces import Box
from stable_baselines3.common.vec_env import VecEnvWrapper
from stable_baselines3.common.vec_env.base_vec_env import VecEnvStepReturn


class ObservationOption2Wrapper(Wrapper):
    # def step_wait(self) -> VecEnvStepReturn:
    #    pass

    def __init__(self, env):
        super().__init__(env)
        # 1. Power Output 2. WP1 RPM 3. CP/moderator Percentage
        self.observation_space = Box(np.array([-1, -1, -1]).astype(np.float32), np.array([1, 1, 1]).astype(np.float32))

    def step(self, action):
        original_result = list(self.env.step(action))
        normalized_rpm = 2 * (self.state.full_reactor.water_pump1.rpm / 2000) - 1
        normalized_moderator_percent = 2 * (self.state.full_reactor.reactor.moderator_percent / 100) - 1
        original_result[0] = np.append(
            original_result[0], np.array([float(normalized_rpm), float(normalized_moderator_percent)])
        )
        return tuple(original_result)

    def reset(self):
        return np.append(self.env.reset(), np.array([float(-1), float(1)]))
