from .flow import Flow
from .mode_service import ModeService
from .type_service import Type


class ModeServiceDevice(ModeService):
    def __init__(self, time_work: float, time_service: float, type: Type = Type.DEFAULT_MODE) -> None:
        self.time_work = time_work
        self.time_service = time_service
        self.mode = type

    def service(self, flow_cars: Flow, start_time: float = 0):
        # TODO
        return self.time_work + start_time
