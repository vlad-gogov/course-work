from .flow import Flow
from .mode_service import ModeService
from .type_service import Type


class ModeServiceDevice(ModeService):
    def __init__(self, time_work: float, time_service: float, type: Type = Type.DEFAULT_MODE) -> None:
        self.time_work = time_work
        self.time_service = time_service  # Время обслуживания одной заявки
        self.mode = type

    def service(self, flow_cars: Flow, start_time: float = 0, delta: float = 0):
        t = start_time
        # Число потенциально обслужанных машин
        l = min(int((self.time_work + delta) / self.time_service),
                len(flow_cars.cars))
        for i in range(l):
            if (flow_cars.cars[0][0] < start_time + self.time_work):
                print(i, ":", flow_cars.cars)
                lengh_pack = len(flow_cars.cars[0])
                if (lengh_pack == 1):
                    flow_cars.add_gamma(max((t - flow_cars.cars[0][0]), 0))
                    t += self.time_service
                else:
                    flow_cars.add_gamma(
                        lengh_pack * max((t - flow_cars.cars[0][-1]), 0), lengh_pack)
                    t += self.time_service + \
                        (flow_cars.cars[0][-1] - flow_cars.cars[0][0])
                flow_cars.cars = flow_cars.cars[1:]
            else:
                break
        print(self.time_work + start_time, ":", flow_cars.cars)
        return self.time_work + start_time
