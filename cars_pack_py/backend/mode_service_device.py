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
        new_time_work = (self.time_work if delta == 0 else delta)
        l = min(int(new_time_work / self.time_service),
                len(flow_cars.cars))
        print(len(flow_cars.cars))
        if l == 0:
            return new_time_work + start_time
        t = start_time if flow_cars.cars[0] <= start_time else flow_cars.cars[0]
        for x in reversed(flow_cars.cars[:l]):
            if x > start_time + new_time_work:
                l -= 1
            else:
                break
        print("Число обслуживаемых машин: ", l)
        for i in range(l):
            if t <= start_time + new_time_work:
                if flow_cars.cars[0] < start_time + new_time_work - self.time_service:
                    print(i, ":", flow_cars.cars)
                    flow_cars.add_gamma(max((t - flow_cars.cars[0]), 0))
                    print("Время ожидания заявки", flow_cars.cars[0], ":", max(
                        (t - flow_cars.cars[0]), 0))
                    t += self.time_service
                    flow_cars.cars.pop(0)
                elif flow_cars.cars[0] < start_time + new_time_work + self.time_service:
                    print("Обслуживание последних скопившихся машин: ")
                    print(i, ":", flow_cars.cars[:l - i])
                    service_time = self.time_service if t > flow_cars.cars[0] else 0
                    print("Время ожидания заявки",
                          flow_cars.cars[0], ":", service_time)
                    while (i < l):
                        flow_cars.add_gamma(service_time)
                        flow_cars.cars.pop(0)
                        i += 1
                    break
                else:
                    break
            else:
                break
        print("Оставшиеся машины:", flow_cars.cars)
        return new_time_work + start_time
