
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

    def get_gamma(self) -> float:
        return self.y / self.count
