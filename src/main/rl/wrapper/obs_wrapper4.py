import numpy as np
from gym import Wrapper
from gym.spaces import Box


class ObservationOption4Wrapper(Wrapper):
    def __init__(self, env):
        super().__init__(env)
        # 1. Power Output 2. Reactor WaterLevel 3. Reactor Pressure 4. Condenser WaterLevel 5. Condenser Pressure
        self.observation_space = Box(
            np.array([-1, -1, -1, -1, -1]).astype(np.float32), np.array([1, 1, 1, 1, 1]).astype(np.float32)
        )

    def step(self, action):
        original_result = list(self.env.step(action))
        normalized_reactor_water_level = 2 * (self.state.full_reactor.reactor.water_level / 4000) - 1
        normalized_reactor_pressure = 2 * (self.state.full_reactor.reactor.pressure / 550) - 1
        normalized_condenser_water_level = 2 * (self.state.full_reactor.condenser.water_level / 8000) - 1
        normalized_condenser_pressure = 2 * (self.state.full_reactor.condenser.pressure / 180) - 1

        original_result[0] = np.append(
            original_result[0],
            np.array(
                [
                    float(normalized_reactor_water_level),
                    float(normalized_reactor_pressure),
                    float(normalized_condenser_water_level),
                    float(normalized_condenser_pressure),
                ]
            ),
        )
        return tuple(original_result)

    def reset(self):
        # normalized_reactor_water_level is at start at 50% -> 0; normalized_reactor_pressure is at start at 0 -> -1
        # normalized_condenser_water_level is at start at 50% -> 0; normalized_condenser_pressure is at start at 0 -> -1
        return np.append(self.env.reset(), np.array([float(0), float(-1), float(0), float(-1)]))
