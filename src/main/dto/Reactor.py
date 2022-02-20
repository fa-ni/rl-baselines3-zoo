from collections import deque
from dataclasses import dataclass

from src.main.dto.ReactorComponent import ReactorComponent


@dataclass
class Reactor(ReactorComponent):
    _water_level: float
    _pressure: float
    _overheated: bool
    _moderator_percent: int
    _melt_stage: int
    _poisoning_factor: deque

    MAX_WATER_LEVEL = 2400
    CRITICAL_WATER_LEVEL_THRESHOLD = 1000
    MAX_PRESSURE = 500

    def __init__(
        self,
        water_level: float,
        pressure: float,
        overheated: bool,
        moderator_percent: int,
        melt_stage: int,
    ):
        self._water_level = water_level
        self._pressure = pressure
        self._overheated = overheated
        self._moderator_percent = moderator_percent
        self._melt_stage = melt_stage
        self._poisoning_factor = deque(maxlen=100)
        [self._poisoning_factor.append(moderator_percent) for _ in range(100)]
        super().__init__(False)

    def meltdown(self):
        self._overheated = True
        self._melt_stage = 5

    # This is also named ModeratorPosition in some parts
    @property
    def moderator_percent(self) -> int:
        return self._moderator_percent

    @moderator_percent.setter
    def moderator_percent(self, moderator_percent: int) -> None:
        if moderator_percent > 100:
            moderator_percent = 100
        if moderator_percent < 0:
            moderator_percent = 0
        self._moderator_percent = 100 - moderator_percent
        for _ in range(10):
            self._poisoning_factor.popleft()
            self._poisoning_factor.append(100 - moderator_percent)

    @property
    def overheated(self) -> bool:
        return self._overheated

    @property
    def pressure(self) -> float:
        return self._pressure

    @pressure.setter
    def pressure(self, pressure: float):
        self._pressure = pressure

    @property
    def water_level(self) -> float:
        return self._water_level

    @water_level.setter
    def water_level(self, water_level: float) -> None:
        self._water_level = water_level

    def get_poisoning_factor(self) -> int:
        return self._poisoning_factor[0] - self._moderator_percent
