from dataclasses import dataclass


@dataclass
class ReactorComponent:
    _blown: bool

    def is_blown(self) -> bool:
        return self._blown

    def update(self) -> None:
        pass

    def blown(self) -> None:
        self._blown = True
