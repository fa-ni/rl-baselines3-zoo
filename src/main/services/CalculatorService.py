from src.main.dto.FullReactor import FullReactor
from src.main.dto.Pump import Pump
from src.main.dto.SteamValve import SteamValve

from src.main.dto.WaterValve import WaterValve


class CalculatorService:
    """
    This class has lots of pure functions which are getting the current state of the full_reactor and producing new
    outputs based on the state. These methods are pure function which means that if we pass in the same state multiple
    times, we will always get the same result back. The functions were extracted from the big time_step
    method because they are here easier to understand and test.
    """

    @staticmethod
    def calculate_steam_valve_value(full_reactor: FullReactor, steam_valve: SteamValve, factor: float) -> float:
        if steam_valve.status:
            result = (full_reactor.reactor.pressure - full_reactor.condenser.pressure) / factor
        else:
            result = 0.0
        return result

    @staticmethod
    def calculate_water_valve_value(full_reactor: FullReactor, water_valve: WaterValve, water_pump: Pump) -> float:
        result = 0.0
        if water_valve.status:
            if water_pump.rpm > 0:
                if full_reactor.condenser.water_level > 0:
                    result = water_pump.rpm * 0.07
            else:
                if (
                    full_reactor.condenser.water_level > 0
                    and (full_reactor.condenser.water_level - full_reactor.reactor.water_level) > 470
                    and (full_reactor.steam_valve1.status or full_reactor.steam_valve2.status)
                ):
                    result = 2.0
                elif (
                    full_reactor.condenser.water_level > 0
                    and (full_reactor.condenser.water_level - full_reactor.reactor.water_level) < 470
                    and (full_reactor.steam_valve1.status or full_reactor.steam_valve2.status)
                ):
                    result = -2.0
            if (
                full_reactor.reactor.water_level >= full_reactor.reactor.MAX_WATER_LEVEL + 500
                and not full_reactor.steam_valve1.status
            ):
                result = 0.0

        return result

    @staticmethod
    def calculate_reactor_rest_heat(full_reactor: FullReactor) -> int:
        if full_reactor.reactor.moderator_percent == 100:
            result = int(full_reactor.rest_heat / (1 + full_reactor.RESTHEAT_REDUCING_FACTOR))
        else:
            result = full_reactor.RESTHEAT - (2 * full_reactor.reactor.moderator_percent)
        return result

    @staticmethod
    def calculate_boiled_rw(full_reactor: FullReactor, float_factor: float) -> float:
        boiled_rw: float = (
            (100 - full_reactor.reactor.moderator_percent) * 2 * (900 - full_reactor.reactor.pressure) / 620
        )
        poison = int(
            full_reactor.reactor.get_poisoning_factor() / 5
        )  # TODO Problem in old implementation never is a float
        if full_reactor.reactor.moderator_percent == 100:
            if poison > 0:
                boiled_rw = (boiled_rw + full_reactor.rest_heat) * float_factor * poison
            else:
                boiled_rw = (boiled_rw + full_reactor.rest_heat) * float_factor
        else:
            full_reactor.rest_heat = full_reactor.RESTHEAT - (2 * full_reactor.reactor.moderator_percent)
            if poison > 0:
                boiled_rw = boiled_rw * float_factor * poison
            else:
                boiled_rw = boiled_rw * float_factor
        return boiled_rw
