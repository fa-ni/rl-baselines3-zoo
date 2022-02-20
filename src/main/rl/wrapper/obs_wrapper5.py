import numpy as np
from gym import Wrapper
from gym.spaces import Box


class ObservationOption5Wrapper(Wrapper):
    def __init__(self, env):
        super().__init__(env)
        # 1. Power Output 2. Reactor WaterLevel 3. Reactor Pressure 4. Condenser WaterLevel 5. Condenser Pressure
        # 6. WP1 RPM 7. Moderator_Percent/CR 8. CP RPM 9. WV1 10. SV1
        self.observation_space = Box(
            np.array([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]).astype(np.float32),
            np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).astype(np.float32),
        )

    def step(self, action):
        original_result = list(self.env.step(action))
        normalized_reactor_water_level = 2 * (self.state.full_reactor.reactor.water_level / 4000) - 1
        normalized_reactor_pressure = 2 * (self.state.full_reactor.reactor.pressure / 550) - 1
        normalized_condenser_water_level = 2 * (self.state.full_reactor.condenser.water_level / 8000) - 1
        normalized_condenser_pressure = 2 * (self.state.full_reactor.condenser.pressure / 180) - 1
        normalized_wp1_rpm = 2 * (self.state.full_reactor.water_pump1.rpm / 2000) - 1
        normalized_cr = 2 * (self.state.full_reactor.reactor.moderator_percent / 100) - 1
        normalized_cp_rpm = 2 * (self.state.full_reactor.condenser_pump.rpm / 2000) - 1
        normalized_wv1_status = float(self.state.full_reactor.water_valve1.status)
        normalized_sv1_status = float(self.state.full_reactor.steam_valve1.status)
        normalized_blow_counter = 2 * (self.state.full_reactor.water_pump1.blow_counter / 30) - 1

        original_result[0] = np.append(
            original_result[0],
            np.array(
                [
                    float(normalized_reactor_water_level),
                    float(normalized_reactor_pressure),
                    float(normalized_condenser_water_level),
                    float(normalized_condenser_pressure),
                    float(normalized_wp1_rpm),
                    float(normalized_cr),
                    float(normalized_cp_rpm),
                    float(normalized_wv1_status),
                    float(normalized_sv1_status),
                    float(normalized_blow_counter),
                ]
            ),
        )
        return tuple(original_result)

    # TODO!
    def reset(self):
        sv1_status = -1
        cp_rpm_status = -1
        wv1_status = -1
        if self.action_space.shape[0] <= 3:
            cp_rpm_status = 2 * (1600 / 2000) - 1
            sv1_status = 1
        if self.action_space.shape[0] == 2:
            wv1_status = 1

        return np.append(
            self.env.reset(),
            np.array(
                [
                    float(0),
                    float(-1),
                    float(0),
                    float(-1),
                    float(-1),
                    float(1),
                    float(cp_rpm_status),
                    float(wv1_status),
                    float(sv1_status),
                    float(1),
                ]
            ),
        )
