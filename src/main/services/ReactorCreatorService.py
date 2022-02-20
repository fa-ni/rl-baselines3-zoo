from src.main.dto.Condenser import Condenser
from src.main.dto.FullReactor import FullReactor
from src.main.dto.Generator import Generator
from src.main.dto.Pump import Pump
from src.main.dto.Reactor import Reactor
from src.main.dto.SteamValve import SteamValve
from src.main.dto.Turbine import Turbine
from src.main.dto.WaterValve import WaterValve


class ReactorCreatorService:
    """
    This service creates a full_reactor with the default state and it´s boundaries.
    """

    @staticmethod
    def create_standard_full_reactor() -> FullReactor:
        reactor = Reactor(
            moderator_percent=100,
            overheated=False,
            melt_stage=1,
            pressure=0,
            water_level=2000,
        )
        steam_valve1 = SteamValve(False, False)
        steam_valve2 = SteamValve(False, False)
        water_valve1 = WaterValve(False, False)
        water_valve2 = WaterValve(False, False)
        water_pump1 = Pump(rpm=0, max_rpm=2000, upper_rpm_threshold=1800, blown=False)
        water_pump2 = Pump(rpm=0, max_rpm=2000, upper_rpm_threshold=1800, blown=False)
        condenser_pump = Pump(rpm=0, max_rpm=2000, upper_rpm_threshold=1800, blown=False)
        turbine = Turbine(False)
        condenser = Condenser(_waterLevel=4000, _pressure=0, _blown=False)
        generator = Generator(0, False)

        return FullReactor(
            reactor=reactor,
            steam_valve1=steam_valve1,
            steam_valve2=steam_valve2,
            water_valve1=water_valve1,
            water_valve2=water_valve2,
            water_pump1=water_pump1,
            water_pump2=water_pump2,
            condenser_pump=condenser_pump,
            turbine=turbine,
            condenser=condenser,
            generator=generator,
        )
