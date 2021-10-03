import random

from .model import Model
from . import consts


class ModelBartlet(Model):
    def __init__(self, r=0, g=0) -> None:
        super().__init__()
        if not (0 <= r <= 1 and 0 <= g <= 1):
            raise ValueError()
        self.r = r
        self.g = g

    @staticmethod
    def get_expected_value_custom(r: float, g: float) -> float:
        return 1 + (r / (1 - g))

    def get_expected_value(self) -> float:
        return 1 + (self.r / (1 - self.g))

    def get_probability(self, k: int) -> float:
        if k == 1:
            return 1 - self.r
        if k >= 2:
            return self.r * (1 - self.g) * self.g ** (k - 2)
        return 0

    def count_requests(self) -> int:
        count = 0
        p = random.uniform(0, 1 - consts.EPSILON)
        F = 1 - self.r
        l = 0
        temp_g = 1
        temp = self.r * (1 - self.g)
        while F <= p:
            count += 1
            l = temp * temp_g
            F += l
            if abs(l) <= consts.EPSILON:
                return count + 1
            temp_g *= self.g

        return count
