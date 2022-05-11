from .flow import Flow
from .mode_service import ModeService
from .type_service import Type


class ModeChange(ModeService):
    def __init__(self, time_work: float) -> None:
        self.time_work = time_work
        self.mode = Type.PREPARE_MODE

    def service(self, flow_cars: Flow, start_time: float = 0, delta: float = 0):
        return self.time_work + start_time
