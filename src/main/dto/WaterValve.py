from dataclasses import dataclass
from time import sleep

from src.main.dto.ReactorComponent import ReactorComponent


@dataclass
class WaterValve(ReactorComponent):
    _status: bool

    def __init__(self, blown: bool, status: bool):
        self._status = status
        super().__init__(blown)

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, status: bool) -> None:
        if not self._blown:
            self._status = status
