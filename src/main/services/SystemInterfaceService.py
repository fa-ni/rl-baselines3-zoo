import threading

from dto.FullReactor import FullReactor
from services.BackgroundStepService import BackgroundStepService
from services.NPPAutomationService import NPPAutomationService
from services.ReactorCreatorService import ReactorCreatorService


class SystemInterfaceService:
    """
    This is the main services. Compared to the Java version it is just broken up into multiple smaller classes to
    increase understandability and testing. If this service is created, it creates a new default reactor and gets
    one objects each for the two main services (BackgroundStepService and NPPAutomationService) to call the start/run
    function of this services in a separate thread when the "init" method ist called.
    (The BackgroundStepService is not directly started in a new thread but the run method of this class is started
    in a new thread which basically lets the time_step method of the background_service run in a loop
    until the full_reactor has failed (wait==True)).
    """

    _background_step_service: BackgroundStepService
    _full_reactor: FullReactor
    _npp_automation: NPPAutomationService

    def __init__(self):
        self._full_reactor = ReactorCreatorService.create_standard_full_reactor()
        self._background_step_service = BackgroundStepService(reactor=self._full_reactor)
        self._npp_automation = NPPAutomationService(background_step_service=self._background_step_service)

    def init(self, is_active_automation: bool) -> None:
        x = threading.Thread(target=self.start)
        x.start()
        if is_active_automation:
            y = threading.Thread(target=self._npp_automation.run)
            y.start()

    def start(self) -> None:
        while not self._background_step_service.wait:
            self._background_step_service.time_step(n=1)

    @property
    def full_reactor(self) -> FullReactor:
        return self._full_reactor
