import operator
import subprocess
from time import sleep

import pytest
from py4j.java_gateway import JavaGateway

from services.SystemInterfaceService import SystemInterfaceService
from src.main.services.BackgroundStepService import BackgroundStepService
from src.main.services.ReactorCreatorService import ReactorCreatorService
from utils.utils import startup_wo_failing_speedy_python, startup_wo_failing_speedy_java

"""
These tests use the java backend and the python backend implementation to test whether the
time_step method (which is the main logic method of the program) does create identical results
for both implementations.
Therefore different test scenarios are created to tests different paths of the actual method
and check for most of the options.

The corresponding NPP_Simu.jar will be started here within the methods (which is located in the test folder).
To make this test work the used java methods (initSimulation, timeStep) are made public to be accessible
from the outside.

General remarks:
WaterLevel + Pressure are casted to int for the frontend in the java implementation. To check for equality we need
to cast them here in these tests.
We need to invert the expected_blown parameter (if some component is_blown()), because the java interface only
returns the status which is the inverse of the blown parameter (you can find the method in the java code
in the NPPSystemInterface class e.g. getWP1Status which returns the inverse of WP1.blown())
"""


def test_time_step_without_manipulation_expect_no_changes() -> None:
    """
    This method tests if the initSimulation() and the time_step method are equal across both implementations
    without any interruption or changes to the reactor.
    """
    full_reactor = ReactorCreatorService.create_standard_full_reactor()
    background_step_service = BackgroundStepService(full_reactor)
    background_step_service.time_step(2)

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
    backend.timeStep(2)

    assert background_step_service.full_reactor.reactor.moderator_percent == backend.getRodPosition()
    assert int(background_step_service.full_reactor.reactor.pressure) == backend.getPressureReactor()
    assert int(background_step_service.full_reactor.reactor.water_level) == backend.getWaterLevelReactor()
    assert background_step_service.full_reactor.reactor.is_blown() == operator.not_(backend.getReactorStatus())
    assert background_step_service.full_reactor.steam_valve1.status == backend.getSV1Status()
    assert background_step_service.full_reactor.steam_valve2.status == backend.getSV2Status()
    assert background_step_service.full_reactor.water_valve1.status == backend.getWV1Status()
    assert background_step_service.full_reactor.water_valve2.status == backend.getWV2Status()
    assert background_step_service.full_reactor.water_pump1.rpm == backend.getWP1RPM()
    assert background_step_service.full_reactor.water_pump1.is_blown() == operator.not_(backend.getWP1Status())
    assert background_step_service.full_reactor.water_pump2.rpm == backend.getWP2RPM()
    assert background_step_service.full_reactor.water_pump2.is_blown() == operator.not_(backend.getWP2Status())
    assert int(background_step_service.full_reactor.condenser.water_level) == backend.getWaterLevelCondenser()
    assert background_step_service.full_reactor.condenser_pump.rpm == backend.getCPRPM()
    assert int(background_step_service.full_reactor.condenser.pressure) == backend.getPressureCondenser()
    assert background_step_service.full_reactor.condenser.is_blown() == operator.not_(backend.getCondenserStatus())
    assert background_step_service.full_reactor.turbine.is_blown() == operator.not_(backend.getTurbineStatus())
    assert background_step_service.full_reactor.condenser_pump.is_blown() == operator.not_(backend.getKPStatus())
    assert background_step_service.full_reactor.generator.power == backend.getPowerOutlet()
    gateway.shutdown()
    p.kill()


@pytest.mark.parametrize("time_steps", [2, 10, 50])
def test_time_step_with_startup_procedure(time_steps: int) -> None:
    """
    This method tests if the time_step methods are equal across both implementations.
    This scenario uses an actual startup method.
    """
    system_interface = SystemInterfaceService()
    startup_wo_failing_speedy_python(system_interface)
    # Accessing private var
    background_step_service = system_interface._background_step_service
    background_step_service.time_step(time_steps)
    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    gateway = JavaGateway()  # connect to the JVM
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()
    startup_wo_failing_speedy_java(backend)
    backend.timeStep(time_steps)

    assert background_step_service.full_reactor.reactor.moderator_percent == backend.getRodPosition()
    assert int(background_step_service.full_reactor.reactor.pressure) == backend.getPressureReactor()
    assert int(background_step_service.full_reactor.reactor.water_level) == backend.getWaterLevelReactor()
    assert background_step_service.full_reactor.reactor.is_blown() == operator.not_(backend.getReactorStatus())
    assert background_step_service.full_reactor.steam_valve1.status == backend.getSV1Status()
    assert background_step_service.full_reactor.steam_valve2.status == backend.getSV2Status()
    assert background_step_service.full_reactor.water_valve1.status == backend.getWV1Status()
    assert background_step_service.full_reactor.water_valve2.status == backend.getWV2Status()
    assert background_step_service.full_reactor.water_pump1.rpm == backend.getWP1RPM()
    assert background_step_service.full_reactor.water_pump1.is_blown() == operator.not_(backend.getWP1Status())
    assert background_step_service.full_reactor.water_pump2.rpm == backend.getWP2RPM()
    assert background_step_service.full_reactor.water_pump2.is_blown() == operator.not_(backend.getWP2Status())
    assert int(background_step_service.full_reactor.condenser.water_level) == backend.getWaterLevelCondenser()
    assert background_step_service.full_reactor.condenser_pump.rpm == backend.getCPRPM()
    assert int(background_step_service.full_reactor.condenser.pressure) == backend.getPressureCondenser()
    assert background_step_service.full_reactor.condenser.is_blown() == operator.not_(backend.getCondenserStatus())
    assert background_step_service.full_reactor.turbine.is_blown() == operator.not_(backend.getTurbineStatus())
    assert background_step_service.full_reactor.condenser_pump.is_blown() == operator.not_(backend.getKPStatus())
    assert background_step_service.full_reactor.generator.power == backend.getPowerOutlet()
    gateway.shutdown()
    p.kill()


@pytest.mark.parametrize("time_steps", [2, 4, 50])
def test_time_step_with_changing_wp1_and_wv1(time_steps: int) -> None:
    """
    This method tests if the time_step methods are equal across both implementations.
    This scenario changes the wp1 rpm and opens the wv1.
    """
    full_reactor = ReactorCreatorService.create_standard_full_reactor()
    background_step_service = BackgroundStepService(full_reactor)
    background_step_service.full_reactor.water_valve1.status = True
    background_step_service.full_reactor.water_pump1.rpm_to_be_set = 200
    background_step_service.time_step(time_steps)

    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    gateway = JavaGateway()  # connect to the JVM
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()
    backend.setWV1Status(True)
    backend.setWP1RPM(200)
    backend.timeStep(time_steps)
    assert background_step_service.full_reactor.reactor.moderator_percent == backend.getRodPosition()
    assert background_step_service.full_reactor.reactor.pressure == backend.getPressureReactor()
    assert int(background_step_service.full_reactor.reactor.water_level) == backend.getWaterLevelReactor()
    assert background_step_service.full_reactor.reactor.is_blown() == operator.not_(backend.getReactorStatus())
    assert background_step_service.full_reactor.steam_valve1.status == backend.getSV1Status()
    assert background_step_service.full_reactor.steam_valve2.status == backend.getSV2Status()
    assert background_step_service.full_reactor.water_valve1.status == backend.getWV1Status()
    assert background_step_service.full_reactor.water_valve2.status == backend.getWV2Status()
    assert background_step_service.full_reactor.water_pump1.rpm == backend.getWP1RPM()
    assert background_step_service.full_reactor.water_pump1.is_blown() == operator.not_(backend.getWP1Status())
    assert background_step_service.full_reactor.water_pump2.rpm == backend.getWP2RPM()
    assert background_step_service.full_reactor.water_pump2.is_blown() == operator.not_(backend.getWP2Status())
    assert int(background_step_service.full_reactor.condenser.water_level) == backend.getWaterLevelCondenser()
    assert background_step_service.full_reactor.condenser_pump.rpm == backend.getCPRPM()
    assert background_step_service.full_reactor.condenser.pressure == backend.getPressureCondenser()
    assert background_step_service.full_reactor.condenser.is_blown() == operator.not_(backend.getCondenserStatus())
    assert background_step_service.full_reactor.turbine.is_blown() == operator.not_(backend.getTurbineStatus())
    assert background_step_service.full_reactor.condenser_pump.is_blown() == operator.not_(backend.getKPStatus())
    assert background_step_service.full_reactor.generator.power == backend.getPowerOutlet()
    gateway.shutdown()
    p.kill()


@pytest.mark.parametrize("time_steps", [2, 10])
def test_expected_reactor_status_fail(time_steps) -> None:
    """
    This method tests if the time_step methods are equal across both implementations.
    This scenario lets the reactor fail.
    """
    full_reactor = ReactorCreatorService.create_standard_full_reactor()
    background_step_service = BackgroundStepService(full_reactor)
    background_step_service.full_reactor.reactor.moderator_percent = 50
    background_step_service.time_step(time_steps)

    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    gateway = JavaGateway()  # connect to the JVM
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()
    backend.setReactorModeratorPosition(50)
    backend.timeStep(time_steps)
    assert backend.getWaterLevelReactor() == int(background_step_service.full_reactor.reactor.water_level)
    assert backend.getPressureReactor() == int(background_step_service.full_reactor.reactor.pressure)
    assert backend.getPowerOutlet() == background_step_service.full_reactor.generator.power
    assert backend.getReactorStatus() == operator.not_(background_step_service.full_reactor.reactor.overheated)
    gateway.shutdown()
    p.kill()


@pytest.mark.parametrize("time_steps", [10, 50, 75])
def test_expected_turbine_and_wp2_status_fail(
    time_steps,
) -> None:
    """
    This method tests if the time_step methods are equal across both implementations.
    This scenario lets the turbine and the wp2 fail.
    """
    full_reactor = ReactorCreatorService.create_standard_full_reactor()
    background_step_service = BackgroundStepService(full_reactor)
    background_step_service.full_reactor.water_pump2.rpm_to_be_set = 1500
    background_step_service.full_reactor.condenser_pump.rpm_to_be_set = 1500
    background_step_service.full_reactor.water_valve2.status = True
    background_step_service.full_reactor.steam_valve1.status = True
    background_step_service.time_step(time_steps)

    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    gateway = JavaGateway()  # connect to the JVM
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()
    backend.setWP2RPM(1500)
    backend.setCPRPM(1500)
    backend.setWV2Status(True)
    backend.setSV1Status(True)
    backend.timeStep(time_steps)
    assert backend.getWaterLevelReactor() == int(background_step_service.full_reactor.reactor.water_level)
    assert backend.getPressureReactor() == int(background_step_service.full_reactor.reactor.pressure)
    assert backend.getPressureCondenser() == int(background_step_service.full_reactor.condenser.pressure)
    assert backend.getWaterLevelCondenser() == int(background_step_service.full_reactor.condenser.water_level)
    assert backend.getTurbineStatus() == operator.not_(background_step_service.full_reactor.turbine.is_blown())
    assert backend.getWP2Status() == operator.not_(background_step_service.full_reactor.water_pump2.is_blown())
    gateway.shutdown()
    p.kill()


@pytest.mark.parametrize("time_steps", [10, 50, 75])
def test_expected_reactor_max_pressure_fail(
    time_steps,
) -> None:
    """
    This method tests if the time_step methods are equal across both implementations.
    This scenario lets the reactor fail due to too much pressure.
    """
    full_reactor = ReactorCreatorService.create_standard_full_reactor()
    background_step_service = BackgroundStepService(full_reactor)
    background_step_service.full_reactor.reactor.moderator_percent = 15
    background_step_service.full_reactor.water_pump1.rpm_to_be_set = 1000
    background_step_service.full_reactor.water_valve1.status = True

    background_step_service.time_step(time_steps)
    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    gateway = JavaGateway()  # connect to the JVM
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()
    backend.setWP1RPM(1000)
    backend.setWV1Status(True)
    backend.setReactorModeratorPosition(15)

    backend.timeStep(time_steps)

    assert backend.getWaterLevelReactor() == int(background_step_service.full_reactor.reactor.water_level)
    assert backend.getPressureReactor() == int(background_step_service.full_reactor.reactor.pressure)
    assert backend.getWaterLevelCondenser() == int(background_step_service.full_reactor.condenser.water_level)
    assert backend.getPressureCondenser() == int(background_step_service.full_reactor.condenser.pressure)
    assert backend.getReactorTankStatus() == operator.not_(background_step_service.full_reactor.reactor.is_blown())
    gateway.shutdown()
    p.kill()


@pytest.mark.parametrize("time_steps", [10, 50, 75])
def test_expected_turbine_and_wp1_status_fail(
    time_steps,
) -> None:
    """
    This method tests if the time_step methods are equal across both implementations.
    This scenario lets the turbine and wp1 fail.
    """
    full_reactor = ReactorCreatorService.create_standard_full_reactor()
    background_step_service = BackgroundStepService(full_reactor)
    background_step_service.full_reactor.water_pump1.rpm_to_be_set = 1500
    background_step_service.full_reactor.condenser_pump.rpm_to_be_set = 1500
    background_step_service.full_reactor.water_valve1.status = True
    background_step_service.full_reactor.steam_valve1.status = True

    background_step_service.time_step(time_steps)

    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    gateway = JavaGateway()  # connect to the JVM
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()
    backend.setWP1RPM(1500)
    backend.setCPRPM(1500)
    backend.setWV1Status(True)
    backend.setSV1Status(True)
    backend.timeStep(time_steps)
    assert backend.getWaterLevelReactor() == int(background_step_service.full_reactor.reactor.water_level)
    assert backend.getPressureReactor() == int(background_step_service.full_reactor.reactor.pressure)
    assert backend.getWaterLevelCondenser() == int(background_step_service.full_reactor.condenser.water_level)
    assert backend.getPressureCondenser() == int(background_step_service.full_reactor.condenser.pressure)
    assert backend.getTurbineStatus() == operator.not_(background_step_service.full_reactor.turbine.is_blown())
    assert backend.getWP1Status() == operator.not_(background_step_service.full_reactor.water_pump1.is_blown())
    gateway.shutdown()
    p.kill()


@pytest.mark.parametrize("time_steps", [10, 50])
def test_expected_condenser_max_pressure_fail(
    time_steps,
) -> None:
    """
    This method tests if the time_step methods are equal across both implementations.
    This scenario lets condenser fail due to too much pressure fail.
    """
    full_reactor = ReactorCreatorService.create_standard_full_reactor()
    background_step_service = BackgroundStepService(full_reactor)
    background_step_service.full_reactor.water_pump1.rpm_to_be_set = 1000
    background_step_service.full_reactor.water_valve1.status = True
    background_step_service.full_reactor.steam_valve2.status = True
    background_step_service.full_reactor.reactor.moderator_percent = 15

    background_step_service.time_step(time_steps)
    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    gateway = JavaGateway()  # connect to the JVM
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()
    backend.setWP1RPM(1000)
    backend.setWV1Status(True)
    backend.setSV2Status(True)
    backend.setReactorModeratorPosition(15)

    backend.timeStep(time_steps)

    assert backend.getWaterLevelReactor() == int(background_step_service.full_reactor.reactor.water_level)
    assert backend.getPressureReactor() == int(background_step_service.full_reactor.reactor.pressure)
    assert backend.getWaterLevelCondenser() == int(background_step_service.full_reactor.condenser.water_level)
    assert backend.getPressureCondenser() == int(background_step_service.full_reactor.condenser.pressure)
    assert backend.getCondenserStatus() == operator.not_(background_step_service.full_reactor.condenser.is_blown())
    gateway.shutdown()
    p.kill()
