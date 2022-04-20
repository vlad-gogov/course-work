from os import times_result

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
        new_time_work = (self.time_work if delta == 0 else delta)

        next_time = start_time + new_time_work

        t = start_time
        if len(flow_cars.cars) and flow_cars.cars[0] >= t:
            t = flow_cars.cars[0]

        if self.mode == Type.DETECTOR_MODE:
            self.max_count_service = int(delta / self.time_service)

        for i in range(self.max_count_service):

            if (t >= next_time):
                break

            if flow_cars.queue == 0:
                flow_cars.generation_cars(next_time - t, start_time)

            if (not len(flow_cars.cars)):
                break

            t = flow_cars.cars[0] if t <= flow_cars.cars[0] else t

            if flow_cars.cars[0] < next_time - self.time_service:
                debug_log(i, ":", flow_cars.cars)
                debug_log("Time:", t)
                wait_time = max((t - flow_cars.cars[0]), 0)
                flow_cars.add_gamma(wait_time)
                debug_log("Время ожидания заявки",
                          flow_cars.cars[0], ":", wait_time)
                t += self.time_service
                flow_cars.cars.pop(0)
            # TODO

            elif next_time - self.time_service <= flow_cars.cars[0] <= next_time:
                debug_log("Обслуживание последних скопившихся машин: ")
                debug_log(i, ":", flow_cars.cars[:self.max_count_service - i])
                wait_time = self.time_service if t > flow_cars.cars[0] else 0
                debug_log("Время ожидания заявки",
                          flow_cars.cars[0], ":", wait_time)
                while (i < self.max_count_service and len(flow_cars.cars)):
                    if (flow_cars.cars[0] <= next_time):
                        break
                    flow_cars.add_gamma(wait_time)
                    flow_cars.cars.pop(0)
                    i += 1
                break
            else:
                break

        if t <= next_time:
            self.down_time += next_time - t

        debug_log("Оставшиеся машины:", flow_cars.cars, "\n")
        return next_time
