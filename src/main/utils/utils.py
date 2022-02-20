from time import sleep

from services.SystemInterfaceService import SystemInterfaceService


def log_status_java(backend, time: int):
    print(backend.getPowerOutlet())
    print(backend.getWP1RPM())
    print(backend.getWP2RPM())
    print(backend.getWP1Status())
    print(backend.getWP2Status())
    print(backend.getCPRPM())
    print(backend.getCPStatus())
    print(backend.getRodPosition())
    print(backend.getWaterLevelCondenser())
    print(backend.getPressureCondenser())
    print(backend.getWaterLevelReactor())
    print(backend.getCondenserStatus())
    print(backend.getPressureReactor())
    print(backend.getReactorStatus())
    print(backend.getReactorTankStatus())
    print(backend.getTurbineStatus())
    print(backend.getSV1Status())
    print(backend.getSV2Status())
    print(backend.getWV1Status())
    print(backend.getWV2Status())
    print(backend.getAtomicStatus())
    sleep(time)


def startup_wo_failing_speedy_java(backend) -> None:
    backend.setSV2Status(True)
    backend.setCPRPM(1600)
    backend.setWV1Status(True)
    backend.setWP1RPM(200)
    backend.setReactorModeratorPosition(5)
    backend.setSV1Status(True)
    backend.setSV2Status(False)
    for i in range(5, 60):
        backend.setReactorModeratorPosition(i)
        speed = 180 + i * 50 if (180 + i * 50) < 2000 else 2000
        backend.setWP1RPM(speed)
        log_status_java(backend, 0)
    backend.setWP1RPM(1620)
    backend.setReactorModeratorPosition(60)


def startup_wo_failing_speedy_python(backend: SystemInterfaceService) -> None:
    backend.full_reactor.steam_valve2.status = True
    backend.full_reactor.condenser_pump.rpm_to_be_set = 1600
    backend.full_reactor.water_valve1.status = True
    backend.full_reactor.water_pump1.rpm_to_be_set = 200
    backend.full_reactor.reactor.moderator_percent = 5
    backend.full_reactor.steam_valve1.status = True
    backend.full_reactor.steam_valve2.status = False
    for i in range(5, 60):
        backend.full_reactor.reactor.moderator_percent = i
        speed = 180 + i * 50 if (180 + i * 50) < 2000 else 2000
        backend.full_reactor.water_pump1.rpm_to_be_set = speed
        log_status_python(backend, 0)
    backend.full_reactor.water_pump1.rpm_to_be_set = 1620
    backend.full_reactor.reactor.moderator_percent = 60


def log_status_python(backend, time):
    print(backend.full_reactor.generator.power)
    print(backend.full_reactor.water_pump1.rpm)
    print(backend.full_reactor.water_pump2.rpm)
    print(backend.full_reactor.condenser_pump.rpm)
    print(backend.full_reactor.reactor.moderator_percent)
    print(backend.full_reactor.condenser.water_level)
    print(backend.full_reactor.condenser.pressure)
    print(backend.full_reactor.reactor.water_level)
    print(backend.full_reactor.reactor.overheated)
    print(backend.full_reactor.reactor.is_blown())
    print(backend.full_reactor.condenser.is_blown())
    print(backend.full_reactor.turbine.is_blown())
    print(backend.full_reactor.water_pump1.is_blown())
    print(backend.full_reactor.water_pump2.is_blown())
    print(backend.full_reactor.condenser_pump.is_blown())
    print(backend.full_reactor.get_atomic_status())
    print(backend.full_reactor.reactor.pressure)
    print(backend.full_reactor.steam_valve1.status)
    print(backend.full_reactor.water_valve1.status)
    print(backend.full_reactor.steam_valve2.status)
    print(backend.full_reactor.water_valve1.status)
    sleep(time)
