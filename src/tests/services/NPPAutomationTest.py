import subprocess
import threading
from time import sleep

import pytest
from py4j.java_gateway import JavaGateway

from src.main.services.BackgroundStepService import BackgroundStepService
from src.main.services.NPPAutomationService import NPPAutomationService
from src.main.services.ReactorCreatorService import ReactorCreatorService

"""
This tests use the java backend and the python backend implementation to test whether the
npp_automation class with the run method does create identical results
for both implementations.
Therefore different test scenarios are created to tests different paths of the actual method
and check for most of the options.

The corresponding NPP_Simu.jar will be started here within the methods. To make this test work the  used java methods
(initSimulation, timeStep) are made public to be accessible from the outside.
These tests are hard to execute. In the background there is no other thread allowed. If you execute the tests multiple
times, it sometimes happens that a thread is not correctly closed and causes the test to
fail in the next iteration. So stop everything again, rebuild and start java version and then try again.
"""


@pytest.mark.parametrize("time_steps_after_setup", [1, 15])
def test_npp_automation_delta_smaller_0_java(time_steps_after_setup: int) -> None:
    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    gateway = JavaGateway()
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()
    backend.setWP1RPM(400)
    backend.setReactorModeratorPosition(10)
    backend.timeStep(5)

    automation = system_interface.getAutomation(backend)
    automation.start()
    backend.timeStep(time_steps_after_setup)
    # Needs some time to run some iterations of the npp automation in the background
    sleep(3)
    java_rod_pos = backend.getRodPosition()
    java_wp1_rom = backend.getWP1SetRPM()
    backend.stopp()
    gateway.shutdown()
    p.kill()

    full_reactor = ReactorCreatorService.create_standard_full_reactor()
    background_step_service = BackgroundStepService(full_reactor)
    background_step_service.full_reactor.water_pump1.rpm_to_be_set = 400
    background_step_service.full_reactor.reactor.moderator_percent = 10
    background_step_service.time_step(5)
    automation = NPPAutomationService(background_step_service)

    x = threading.Thread(target=automation.run, daemon=True)
    x.start()
    # Needs minimal time to start thread
    sleep(1)
    background_step_service.time_step(time_steps_after_setup)
    # Needs some time to run some iterations of the npp automation in the background
    sleep(3)
    assert background_step_service.full_reactor.water_pump1.rpm_to_be_set == java_wp1_rom
    assert background_step_service.full_reactor.reactor.moderator_percent == java_rod_pos
    # Stopping thread
    background_step_service.stop()


@pytest.mark.parametrize("time_steps_after_setup", [10, 18])
def test_npp_automation_delta_equal_and_bigger_than_0_python(
    time_steps_after_setup: int,
) -> None:
    full_reactor = ReactorCreatorService.create_standard_full_reactor()
    background_step_service = BackgroundStepService(full_reactor)
    background_step_service.full_reactor.water_pump1.rpm_to_be_set = 800
    background_step_service.full_reactor.water_valve1.status = True
    background_step_service.time_step(5)
    automation = NPPAutomationService(background_step_service)
    x = threading.Thread(target=automation.run, daemon=True)
    x.start()
    # Needs minimal time to start thread
    sleep(0.5)
    background_step_service.time_step(time_steps_after_setup)
    # Needs some time to run some iterations of the npp automation in the background
    sleep(2)
    python_wp1_rpm = background_step_service.full_reactor.water_pump1.rpm_to_be_set
    # Stopping thread
    background_step_service.stop()

    p = subprocess.Popen(
        [
            "java",
            "-jar",
            "NPP_Simu.jar",
        ]
    )
    sleep(1)
    gateway = JavaGateway()
    system_interface = gateway.entry_point
    backend = system_interface.getSystemInterface()
    backend.initSimulation()
    backend.setWP1RPM(800)
    backend.setWV1Status(True)
    backend.timeStep(5)

    automation = system_interface.getAutomation(backend)
    automation.start()
    backend.timeStep(time_steps_after_setup)
    # Needs some time to run some iterations of the npp automation in the background
    sleep(1)
    assert backend.getWP1SetRPM() == python_wp1_rpm
    backend.stopp()
    gateway.shutdown()
    p.kill()
