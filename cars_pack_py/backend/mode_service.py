from .type_service import Type
from .flow import Flow


class ModeService():
    def __init__(self, time_work: float):
        self.time_work = time_work
        self.mode = Type.DEFAULT_MODE

    def service(self, flow_cars: Flow, start_time: float = 0, delta: float = 0):
        pass

    def get_type(self):
        return self.mode

    def get_time(self):
        return self.time_work
