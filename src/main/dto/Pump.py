from src.main.dto.ReactorComponent import ReactorComponent


class Pump(ReactorComponent):
    _rpm: int
    _rpm_to_be_set: int
    _blow_counter: int
    _upper_rpm_threshold: int
    _max_rpm: int

    BLOW_COUNTER_INIT = 30

    def __init__(self, rpm: int, upper_rpm_threshold: int, max_rpm: int, blown: bool):
        self._rpm = rpm
        self._rpm_to_be_set = rpm
        self._upper_rpm_threshold = upper_rpm_threshold
        self._max_rpm = max_rpm
        self._blow_counter = self.BLOW_COUNTER_INIT
        super().__init__(blown)

    @property
    def blow_counter(self) -> int:
        return self._blow_counter

    @property
    def rpm_to_be_set(self) -> int:
        return self._rpm_to_be_set

    @rpm_to_be_set.setter
    def rpm_to_be_set(self, rpm: int) -> None:
        if self.is_blown():
            self._rpm_to_be_set = 0
        # This is the slider max in the java implementation
        elif rpm > 2000:
            self._rpm_to_be_set = 2000
        else:
            self._rpm_to_be_set = rpm

    @property
    def rpm(self) -> int:
        return self._rpm

    def blown(self) -> None:
        self._blown = True
        self._rpm = 0
        self._rpm_to_be_set = 0

    def update(self) -> None:
        if not self.is_blown():
            if self._rpm > self._upper_rpm_threshold:
                self._blow_counter -= 1
            elif self._blow_counter < self.BLOW_COUNTER_INIT:
                self._blow_counter += 1
            if self._blow_counter < 0:
                self.blown()
            if self.rpm != self._rpm_to_be_set:
                if self._rpm > self._rpm_to_be_set:
                    self._rpm = self._rpm_to_be_set + int((self._rpm - self._rpm_to_be_set) / 2)
                else:
                    self._rpm = self._rpm_to_be_set - int((self._rpm_to_be_set - self._rpm) / 2)

    @rpm.setter
    def rpm(self, value):
        self._rpm = value
