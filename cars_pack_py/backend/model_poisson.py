import random
import math

from .model import Model
from . import consts


class ModelPoisson(Model):
    def __init__(self, lamb=0, time=0) -> None:
        super().__init__()
        self.lamb = lamb
        self.time = time

    def _is_correct(self, count_requests: int, time: float) -> bool:
        return abs(count_requests / time - self.lamb) < 0.1 * self.lamb

    def count_requests(self) -> int:
        count = 0
        a = self.lamb * self.time
        p = random.uniform(0, 1 - consts.EPSILON) * math.exp(a)
        if abs(1 - p) <= consts.EPSILON:
            return 0
        l = 1
        F = l
        while F <= p:
            count += 1
            l *= a / count
            if l <= consts.EPSILON:
                return count
            F += l
        return count