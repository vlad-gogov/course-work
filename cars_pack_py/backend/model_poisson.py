import numpy
import math

from .model import Model
from . import consts


class ModelPoisson(Model):
    def __init__(self, lamb=0, time=0) -> None:
        super().__init__()
        if not (0 <= lamb <= 1):
            raise ValueError()
        self.lamb = lamb
        self.time = time

    def _is_correct(self, count_requests: int, time: float) -> bool:
        return abs(count_requests / time - self.lamb) < 0.1 * self.lamb

    def count_requests(self) -> int:
        count = 0
        a = self.lamb * self.time
        p = numpy.random.uniform(0, 1 - consts.EPSILON) * math.exp(a)
        l = 1
        F = l
        while F <= p:
            count += 1
            l *= a / count
            if l <= consts.EPSILON:
                return count
            F += l
        return count
