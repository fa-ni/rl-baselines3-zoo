import gym as gym

from src.main.rl.utils.utils import is_done
from src.main.rl.wrapper.reward_calculations import calculate_roofed_reward, calculate_reward_for_corridor


class RewardOption3Wrapper(gym.RewardWrapper):
    def __init__(self, env):
        super().__init__(env)

    def reward(self, rew: float) -> float:
        result = 0
        done = is_done(self.state.full_reactor, self.length)  # Maybe also set it as a class variable? TODO
        if not done:
            result_reactor_wl = calculate_reward_for_corridor(1500, 2500, 2100,
                                                              self.state.full_reactor.reactor.water_level)
            result_reactor_pressure = calculate_reward_for_corridor(0, 350, 175,
                                                                    self.state.full_reactor.reactor.pressure)
            # It is not possible to reach critical water level upper bound because we have too few water..
            # result_condenser_wl = calculate_reward_for_corridor(1500, 1, 1,
            #                                                    self.state.full_reactor.condenser.water_level)
            result_condenser_pressure = calculate_reward_for_corridor(0, 80, 40,
                                                                      self.state.full_reactor.condenser.pressure)
            result_corridor = (
                                      result_reactor_wl
                                      + result_reactor_pressure
                                      +
                                      # result_condenser_wl +
                                      result_condenser_pressure
                              ) / 3

            # print(f"Coridor reward: {result_corridor}")
            #result_corridor = result_reactor_wl
            result_power = calculate_roofed_reward(self.state.full_reactor.generator.power)
            result = result_corridor * 0.4 + result_power * 0.6
        return result
