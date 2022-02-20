import operator
import subprocess
from time import sleep

from py4j.java_gateway import JavaGateway

from src.main.services.ReactorCreatorService import ReactorCreatorService


def test_init_simulation() -> None:
    reactor_creator = ReactorCreatorService()
    full_reactor = reactor_creator.create_standard_full_reactor()
    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    # Check if Java program has identical results
    gateway = JavaGateway()  # connect to the JVM
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()

    assert full_reactor.reactor.moderator_percent == backend.getRodPosition()
    assert full_reactor.reactor.pressure == backend.getPressureReactor()
    assert full_reactor.reactor.water_level == backend.getWaterLevelReactor()
    assert full_reactor.reactor.is_blown() == operator.not_(backend.getReactorStatus())
    assert full_reactor.steam_valve1.status == backend.getSV1Status()
    assert full_reactor.steam_valve2.status == backend.getSV2Status()
    assert full_reactor.water_valve1.status == backend.getWV1Status()
    assert full_reactor.water_valve2.status == backend.getWV2Status()
    assert full_reactor.water_pump1.rpm == backend.getWP1RPM()
    assert full_reactor.water_pump1.is_blown() == operator.not_(backend.getWP1Status())
    assert full_reactor.water_pump2.rpm == backend.getWP2RPM()
    assert full_reactor.water_pump2.is_blown() == operator.not_(backend.getWP2Status())
    assert full_reactor.condenser.water_level == backend.getWaterLevelCondenser()
    assert full_reactor.condenser_pump.rpm == backend.getCPRPM()
    assert full_reactor.condenser.pressure == backend.getPressureCondenser()
    assert full_reactor.condenser.is_blown() == operator.not_(backend.getCondenserStatus())
    assert full_reactor.turbine.is_blown() == operator.not_(backend.getTurbineStatus())
    assert full_reactor.condenser_pump.is_blown() == operator.not_(backend.getKPStatus())
    gateway.shutdown()
    p.kill()
