
class Flow():
    def __init__(self) -> None:
        self.cars = []
        self.y = 0  # Времена пребываний машин в системе
        self.y2 = 0  # Квадраты времен пребываний машин в системе
        self.count = 0  # Число обслужанных машин
        self.queue = 0  # Кол-во машин, находящихся в очереди

    def add_gamma(self, Yi: float, count: int = 1) -> None:
        self.y += Yi
        self.y2 += Yi ** 2
        self.count += count
        self.queue -= count

    def add_cars(self, cars_: list, time: float) -> None:
        for car in cars_:
            self.cars.append(car)
            if car <= time:
                self.queue += 1
            else:
                break
        # self.cars.sort()

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

    def get_queue(self, time: float):
        result = 0
        for i in range(len(self.cars)):
            if self.cars[i] <= time:
                result += 1
            else:
                break
        return result
