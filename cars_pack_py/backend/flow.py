
class Flow():
    def __init__(self) -> None:
        self.cars = []
        self.y = 0  # Времяна пребываний машин в системе
        self.count = 0

    def addGamma(self, temp) -> None:
        self.y += temp

    def addCars(self, cars_: list) -> None:
        for car in cars_:
            self.cars.append(car)

    def getGamma(self) -> float:
        return self.sum / self.count
