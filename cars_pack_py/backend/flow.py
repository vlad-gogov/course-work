
class Flow():
    def __init__(self) -> None:
        self.cars = []
        self.y = 0  # Времена пребываний машин в системе
        self.count = 0  # Число обслужанных машин

    def add_gamma(self, Yi: float, count: int = 1) -> None:
        self.y += Yi
        self.count += 1

    def add_cars(self, cars_: list) -> None:
        for car in cars_:
            self.cars.append(car)
        self.cars.sort()

    def get_gamma(self) -> float:
        if self.count <= 0:
            return 0
        return self.y / self.count

    def _reset(self) -> None:
        self.y = 0
        self.count = 0
