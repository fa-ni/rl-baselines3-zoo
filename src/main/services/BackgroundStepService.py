import math
import time

from src.main.dto.FullReactor import FullReactor
from src.main.services.CalculatorService import CalculatorService


class BackgroundStepService:
    """
    This class includes the main logic for the reactor. The time_step method is running as a separate thread to
    continuously run the calculation for the reactor. It calculates all the important values for the reactor and
    defines the interactions and reactions for the important metrics such as water_level, rpm and power output.
    In case the reactor fails, the parameter _wait will be set to True. The full_reactor is the complete reactor with
    all it´s components.
    """

    _full_reactor: FullReactor
    _wait: False

    def __init__(self, reactor: FullReactor):
        self._full_reactor = reactor
        self._wait = False

    def time_step(self, n: int) -> None:
        float_factor = 0.5
        for i in range(n):
            if not self._full_reactor.reactor.overheated:
                v1 = float_factor * CalculatorService.calculate_steam_valve_value(
                    self._full_reactor, self._full_reactor.steam_valve1, 10.0
                )
                # For startup always 0.0
                v2 = float_factor * CalculatorService.calculate_steam_valve_value(
                    self._full_reactor, self._full_reactor.steam_valve2, 2.5
                )
                v3 = float_factor * CalculatorService.calculate_water_valve_value(
                    self._full_reactor,
                    self._full_reactor.water_valve1,
                    self._full_reactor.water_pump1,
                )
                # For startup always 0.0
                v4 = float_factor * CalculatorService.calculate_water_valve_value(
                    self._full_reactor,
                    self._full_reactor.water_valve2,
                    self._full_reactor.water_pump2,
                )

                self._full_reactor.rest_heat = CalculatorService.calculate_reactor_rest_heat(self._full_reactor)
                boiled_rw = CalculatorService.calculate_boiled_rw(self._full_reactor, float_factor)

                cooled_cp: float = float(
                    (self._full_reactor.condenser_pump.rpm * math.sqrt(self._full_reactor.condenser.pressure) * 0.003)
                    * float_factor
                )
                new_rp: float = self._full_reactor.reactor.pressure - v1 - v2 + boiled_rw / 4
                if self._full_reactor.turbine.is_blown():
                    v1 = 0.0

                # Calculating new values for pressure and water_level
                new_cp: float = self._full_reactor.condenser.pressure + v1 + v2 - cooled_cp
                new_rw: float = self._full_reactor.reactor.water_level + v3 + v4 - boiled_rw
                new_cw: float = self._full_reactor.condenser.water_level - v3 - v4 + 4 * cooled_cp

                # Adjustment for blown tasks
                if self._full_reactor.reactor.is_blown():
                    new_rp = 0.15 * new_rp
                if self._full_reactor.condenser.is_blown():
                    new_cp = 0.2 * new_cp

                # Check and adjust value
                if new_cw < 0:
                    new_cw = 0
                if new_cw > 9600:
                    new_cw = 9600
                if new_cp < 0:
                    new_cp = 0
                if new_cp > 300:
                    new_cp = 300
                if new_rp > 800:
                    new_rp = 800
                if new_rw > 4700:
                    new_rw = 4700
                # Adjusting generator power
                new_effect: float = 0
                if self._full_reactor.steam_valve1.status and not self._full_reactor.turbine.is_blown():
                    new_effect = (new_rp - new_cp) * 2.5

                # Assign values
                self._full_reactor.generator.power = int(new_effect)
                self._full_reactor.condenser.pressure = new_cp
                self._full_reactor.condenser.water_level = new_cw
                self._full_reactor.reactor.pressure = new_rp
                self._full_reactor.reactor.water_level = new_rw
                # Rules
                self._check_and_set_failure()
                # NOTE: This is handled with a for loop over each component in java implementation
                self._full_reactor.water_pump1.update()
                self._full_reactor.water_pump2.update()
                self._full_reactor.condenser_pump.update()

    def _check_and_set_failure(self) -> None:
        if self._full_reactor.water_pump1.is_blown():
            self._full_reactor.water_pump1.rpm_to_be_set = 0
        if self._full_reactor.water_pump2.is_blown():
            self._full_reactor.water_pump2.rpm_to_be_set = 0
        if self._full_reactor.condenser_pump.is_blown():
            self._full_reactor.condenser_pump.rpm_to_be_set = 0
        if self._full_reactor.reactor.water_level < self._full_reactor.reactor.CRITICAL_WATER_LEVEL_THRESHOLD:
            self._full_reactor.reactor.meltdown()
        if self._full_reactor.reactor.pressure >= self._full_reactor.reactor.MAX_PRESSURE:
            self._full_reactor.reactor.blown()
        if (
            self._full_reactor.reactor.water_level > self._full_reactor.reactor.MAX_WATER_LEVEL + 500
            and self._full_reactor.steam_valve1.status
        ):
            self._full_reactor.turbine.blown()
        if (
            self._full_reactor.condenser.water_level <= self._full_reactor.condenser.MIN_WATER_LEVEL
            and self._full_reactor.water_pump1.rpm > 0
        ):
            self._full_reactor.water_pump1.blown()
        if (
            self._full_reactor.condenser.water_level <= self._full_reactor.condenser.MIN_WATER_LEVEL
            and self._full_reactor.water_pump2.rpm > 0
        ):
            self._full_reactor.water_pump2.blown()
        if self._full_reactor.condenser.pressure >= self._full_reactor.condenser.MAX_PRESSURE:
            self._full_reactor.condenser.blown()
        if self._full_reactor.condenser.water_level > self._full_reactor.condenser.MAX_WATER_LEVEL + 300:
            self._full_reactor.turbine.blown()

    @property
    def full_reactor(self) -> FullReactor:
        return self._full_reactor

    @property
    def wait(self) -> bool:
        return self._wait

    def stop(self) -> None:
        self._wait = True
