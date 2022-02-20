from time import sleep

from src.main.services.BackgroundStepService import BackgroundStepService


class NPPAutomationService:
    """
    This class runs in the background as another thread to also continuously evaluate and executes the run function
    unless the reactor fails and the wait parameter of the simulation is set to True. This service interferes and
    sets more boundaries to the full_reactor state.
    """

    _simulator: BackgroundStepService

    def __init__(self, background_step_service: BackgroundStepService) -> None:
        self._simulator = background_step_service
        self._running = True

    def run(self) -> None:
        wl1: int = int(self._simulator.full_reactor.reactor.water_level)
        while not self._simulator.wait:
            if (
                self._simulator.full_reactor.reactor.water_level > 2500
                or self._simulator.full_reactor.reactor.water_level < 1900
            ):
                delta_wl: int = int(self._simulator.full_reactor.reactor.water_level) - wl1
                print(f"delta water level: {delta_wl}")

                if delta_wl < 0:
                    new_rpm: int = int(
                        self._simulator.full_reactor.water_pump1.rpm
                        + abs(delta_wl)
                        + abs(int(self._simulator.full_reactor.reactor.water_level) - 2200)
                    )
                    if self._simulator.full_reactor.reactor.water_level < 2200 and new_rpm >= 0:
                        self._simulator.full_reactor.water_pump1.rpm_to_be_set = new_rpm
                elif delta_wl > 0:
                    new_rpm: int = int(
                        self._simulator.full_reactor.water_pump1.rpm
                        - abs(delta_wl)
                        + abs(self._simulator.full_reactor.reactor.water_level - 2200)
                    )
                    if self._simulator.full_reactor.reactor.water_level < 2200 and new_rpm >= 0:
                        self._simulator.full_reactor.water_pump1.rpm_to_be_set = new_rpm
                else:
                    if self._simulator.full_reactor.reactor.water_level > 2200:
                        self._simulator.full_reactor.water_pump1.rpm_to_be_set = 0
                    if self._simulator.full_reactor.reactor.water_level < 1800:
                        self._simulator.full_reactor.water_pump1.rpm_to_be_set = 1800

            if (
                self._simulator.full_reactor.reactor.water_level > 2800
                or self._simulator.full_reactor.reactor.water_level < 1500
            ):
                self._simulator.full_reactor.reactor.moderator_percent = 0
            wl1 = int(self._simulator.full_reactor.reactor.water_level)
            sleep(0.25)
