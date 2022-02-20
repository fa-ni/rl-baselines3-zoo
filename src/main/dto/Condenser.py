from dataclasses import dataclass

from src.main.dto.ReactorComponent import ReactorComponent


@dataclass
class Condenser(ReactorComponent):
    MIN_WATER_LEVEL = 300
    MAX_WATER_LEVEL = 5000
    MIN_PRESSURE = 0
    MAX_PRESSURE = 140
    UPPER_PRESSURE_THRESHOLD = 120
    _waterLevel: float
    _pressure: float

    @property
    def water_level(self) -> float:
        return self._waterLevel

    @water_level.setter
    def water_level(self, water_level: float):
        self._waterLevel = water_level

    @property
    def pressure(self) -> float:
        return self._pressure

    @pressure.setter
    def pressure(self, pressure: float) -> None:
        self._pressure = pressure
