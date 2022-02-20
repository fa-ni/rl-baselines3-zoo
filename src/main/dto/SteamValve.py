from dataclasses import dataclass
from time import sleep

from src.main.dto.ReactorComponent import ReactorComponent


@dataclass
class SteamValve(ReactorComponent):
    _status: bool

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, status: bool) -> None:
        self._status = status
