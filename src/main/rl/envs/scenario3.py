import numpy as np
from gym import Env
from gym.spaces import Box, MultiDiscrete

from src.main.rl.utils.utils import is_done
from src.main.services.BackgroundStepService import BackgroundStepService
from src.main.services.ReactorCreatorService import ReactorCreatorService


class Scenario3(Env):
    # Scenario 3 with MultiDiscrete Action Spaces
    # if no wrapper is specified this will use ActionSpaceOption 1 and ObservationSpaceOption1
    def __init__(self):
        # 1. moderator_percent 2. WP1 RPM
        self.action_space = MultiDiscrete([3, 3])
        self.observation_space = Box(np.array([-1]).astype(np.float32), np.array([1]).astype(np.float32))
        self.length = 250

    def step(self, action):
        reward = 0
        self.length -= 1

        # Standard/Minimal Actions (Option 1 Actions)
        moderator_percent_setting = -1 if action[0] == 0 else (0 if action[0] == 1 else 1)
        wp_rpm_setting = -25 if action[1] == 0 else (0 if action[1] == 1 else 25)
        self.state.full_reactor.reactor.moderator_percent = (
            100 - self.state.full_reactor.reactor.moderator_percent + moderator_percent_setting
        )
        if wp_rpm_setting + self.state.full_reactor.water_pump1.rpm_to_be_set > 0:
            self.state.full_reactor.water_pump1.rpm_to_be_set += wp_rpm_setting
        else:
            self.state.full_reactor.water_pump1.rpm_to_be_set += 0

        # Necessary for Action Space Option 1
        if len(action) == 2:
            # This is necessary as you cannot override the state from this environment in any of the wrappers
            if self.length == 249:
                self.state.full_reactor.condenser_pump.rpm = 1600
                self.state.full_reactor.steam_valve1.status = True
                self.state.full_reactor.water_valve1.status = True
            self.state.full_reactor.condenser_pump.rpm_to_be_set = 1600
            self.state.full_reactor.steam_valve1.status = True
            self.state.full_reactor.water_valve1.status = True
        # Necessary for Action Space Option 2
        if len(action) == 3:  # TODO
            # This is necessary as you cannot override the state from this environment in any of the wrappers
            if self.length == 249:
                self.state.full_reactor.condenser_pump.rpm = 1600
                self.state.full_reactor.steam_valve1.status = True
            self.state.full_reactor.condenser_pump.rpm_to_be_set = 1600
            self.state.full_reactor.steam_valve1.status = True
            water_valve_setting = (
                False if action[2] == 0 else (self.state.full_reactor.water_valve1.status if action[2] == 1 else True)
            )
            self.state.full_reactor.water_valve1.status = water_valve_setting
        # Necessary for Action Space Option 3
        if len(action) == 5:  # TODO
            water_valve_setting = (
                False if action[2] == 0 else (self.state.full_reactor.water_valve1.status if action[2] == 1 else True)
            )
            steam_valve_setting = (
                False if action[3] == 0 else (self.state.full_reactor.steam_valve1.status if action[3] == 1 else True)
            )
            condenser_rpm_setting = -25 if action[4] == 0 else (0 if action[4] == 1 else +25)
            self.state.full_reactor.water_valve1.status = water_valve_setting
            self.state.full_reactor.steam_valve1.status = steam_valve_setting
            self.state.full_reactor.condenser_pump.rpm_to_be_set += condenser_rpm_setting
        self.state.time_step(1)

        done = is_done(self.state.full_reactor, self.length)
        if not done:
            calc_reward = self.state.full_reactor.generator.power / 700
            reward += calc_reward  # TODO calc_reward if calc_reward < 1 else 1

        normalized_obs = 2 * (self.state.full_reactor.generator.power / 800) - 1
        return [
            # Might need to change if we dont want to have binary for first observation
            np.array([normalized_obs]),
            reward,
            done,
            {},
        ]

    def render(self):
        pass

    def reset(self):
        self.state = None
        self.state = BackgroundStepService(ReactorCreatorService.create_standard_full_reactor())
        self.moderator_percent = 100
        self.length = 250
        return np.array([float(-1)])
