from .flow import Flow
from .mode_service import ModeService
from .type_service import Type


class ModeServiceDevice(ModeService):
    def __init__(self, time_work: float, time_service: float, type: Type = Type.DEFAULT_MODE) -> None:
        self.time_work = time_work
        self.time_service = time_service  # Время обслуживания одной заявки
        self.mode = type

    def service(self, flow_cars: Flow, start_time: float = 0, delta: float = 0):
        # Число потенциально обслужанных машин
        l = min(int((self.time_work + delta) / self.time_service),
                len(flow_cars.cars))
        if l == 0:
            return self.time_work + start_time
        t = flow_cars.cars[0]
        for x in reversed(flow_cars.cars[:l]):
            if x >= start_time + self.time_work:
                l -= 1
            else:
                break
        for i in range(l):
            if start_time <= t <= start_time + self.time_work:
                if (flow_cars.cars[0] < start_time + self.time_work - self.time_service):
                    print(i, ":", flow_cars.cars)
                    flow_cars.add_gamma(max((t - flow_cars.cars[0]), 0))
                    t += self.time_service
                    flow_cars.cars.pop(0)
                else:
                    print("Обслуживание последних скопившихся машин: ")
                    print(i, ":", flow_cars.cars[:l - i])
                    print("t: ", t)
                    service_time = self.time_service if t > flow_cars.cars[0] else 0
                    while (i < l):
                        flow_cars.add_gamma(service_time)
                        flow_cars.cars.pop(0)
                        i += 1
                    break
            else:
                break
        print("Оставшиеся машины:", flow_cars.cars)
        return self.time_work + start_time
