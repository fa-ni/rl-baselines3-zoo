from dataclasses import dataclass

from src.main.dto.ReactorComponent import ReactorComponent


@dataclass
class Generator(ReactorComponent):
    _power: int

    @property
    def power(self) -> int:
        return self._power

    @power.setter
    def power(self, p: int) -> None:
        if not self.is_blown():
            self._power = p
        else:
            self._power = 0
