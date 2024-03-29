from .flow import Flow
from .mode_service import ModeService
from .type_service import Type
from .utils import debug_log


class ModeServiceDevice(ModeService):
    def __init__(self, time_work: float, time_service: float, type: Type = Type.SERVICE_MODE) -> None:
        self.time_work = time_work
        self.time_service = time_service  # Время обслуживания одной заявки
        self.max_count_service = int(self.time_work / self.time_service)
        self.mode = type
        self.down_time = 0

    def service(self, flow_cars: Flow, start_time: float = 0, delta: float = 0):
        # Число потенциально обслужанных машин
        new_time_work = self.time_work + delta

        if delta != 0:
            self.max_count_service = int(new_time_work / self.time_service)

        next_time = start_time + new_time_work

        t = start_time
        if len(flow_cars.cars) and flow_cars.cars[0] >= t:
            t = flow_cars.cars[0]

        for i in range(self.max_count_service):

            if (t >= next_time):
                break

            if (not len(flow_cars.cars)):
                break

            t = flow_cars.cars[0] if t <= flow_cars.cars[0] else t

            if flow_cars.cars[0] < next_time - self.time_service:
                wait_time = max((t - flow_cars.cars[0]), 0)
                flow_cars.add_gamma(wait_time)
                t += self.time_service

            elif next_time - self.time_service <= flow_cars.cars[0] <= next_time:
                wait_time = self.time_service if t > flow_cars.cars[0] else 0
                while (i < self.max_count_service and len(flow_cars.cars)):
                    if (flow_cars.cars[0] <= next_time):
                        break
                    flow_cars.add_gamma(wait_time)
                    i += 1
                t += self.time_service
                break
            else:
                break

        if next_time - delta <= t <= next_time and delta != 0:
            self.down_time += next_time - t

        self.max_count_service = int(self.time_work / self.time_service)

        return next_time
