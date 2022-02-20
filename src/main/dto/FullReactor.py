from dataclasses import dataclass

from src.main.dto.Condenser import Condenser
from src.main.dto.Generator import Generator
from src.main.dto.Pump import Pump
from src.main.dto.Reactor import Reactor
from src.main.dto.SteamValve import SteamValve
from src.main.dto.Turbine import Turbine
from src.main.dto.WaterValve import WaterValve


@dataclass
class FullReactor:
    reactor: Reactor
    steam_valve1: SteamValve
    steam_valve2: SteamValve
    water_valve1: WaterValve
    water_valve2: WaterValve
    water_pump1: Pump
    water_pump2: Pump
    condenser_pump: Pump
    turbine: Turbine
    condenser: Condenser
    generator: Generator

    RESTHEAT = 200
    RESTHEAT_REDUCING_FACTOR = 0.0001

    rest_heat = 0
    normal_state = 3
    state = normal_state
    wait = False

    def get_atomic_status(self) -> bool:
        if self.reactor.overheated and (
            self.reactor.is_blown() or self.condenser.is_blown() or self.turbine.is_blown()
        ):
            return False
        else:
            return True
