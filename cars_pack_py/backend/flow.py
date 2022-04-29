from .car_flow import CarFlow


class Flow():
    def __init__(self, lamb: float, r: float, g: float) -> None:
        if not (0 <= lamb <= 1 and 0 <= r <= 1 and 0 <= g <= 1):
            raise ValueError()
        self.lamb = lamb
        self.r = r
        self.g = g
        self.cars = []
        self.y = 0  # Сумма времен пребываний машин в системе
        self.y2 = 0  # Квадраты времен пребываний машин в системе
        self.count = 0  # Число обслужанных машин
        self.queue = 0  # Очередь по потоку

    def add_gamma(self, Yi: float, count: int = 1) -> None:
        self.y += Yi
        self.y2 += Yi ** 2
        self.count += count
        self.queue -= count

    def generation_cars(self, generation_interval: float, start_time: float = 0) -> None:
        car_flow = CarFlow(self.lamb, generation_interval, self.r, self.g)
        cars_ = car_flow.create_flow(True)
        for car in cars_:
            self.cars.append(car + start_time)
        self.queue += len(cars_)

    def add_cars(self, car: float) -> None:
        self.cars.append(car)

    def get_gamma(self) -> float:
        if self.count <= 0:
            return 0
        return self.y / self.count

    def get_dispersion(self) -> float:
        if self.count <= 0:
            return 0
        gamma = self.get_gamma()
        return self.y2 / self.count - gamma ** 2

    def _reset(self) -> None:
        self.y = 0
        self.y2 = 0
        self.count = 0
        self.cars.clear()
