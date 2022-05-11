from . import consts
from .model_poisson import ModelPoisson
from .model_bartlet import ModelBartlet

import numpy


class CarFlow:
    def __init__(self, lamb: float = 0, time: float = 0, r: float = 0, g: float = 0) -> None:
        self.lamb = lamb
        self.time = time
        self.r = r
        self.g = g

    def _create_cars_slow(self) -> numpy.ndarray:
        all_count_requests = 0
        lambda_b = self.lamb / (1 + self.r/(1 - self.g))
        model = ModelPoisson(lambda_b, self.time)
        all_count_requests = model.count_requests()
        slow_cars = numpy.random.uniform(0, 1, [all_count_requests])
        slow_cars *= self.time
        slow_cars = numpy.sort(slow_cars)
        return slow_cars

    def _build_pack(self, average_pack_length: float, time_start: float, count_fast_cars: int):
        pack = []
        for _ in range(count_fast_cars):
            time_moment = time_start + \
                numpy.random.uniform(0, 1) * average_pack_length
            while time_moment > self.time:
                time_moment = time_start + \
                    numpy.random.uniform(0, 1) * average_pack_length
            pack.append(time_moment)
        pack.sort()
        return pack

    def create_flow(self, mode: bool = False) -> numpy.ndarray:
        # Slow cars
        slow_cars = self._create_cars_slow()
        count_pack = len(slow_cars)

        if self.r == 0 or count_pack == 0:
            return slow_cars

        # Fast cars
        flow_cars = [[car] for car in slow_cars]

        c = 2
        model_bartlet = ModelBartlet(self.r, self.g)
        average_pack_length = 0
        count_fast_car = []
        delta_min_time = 1e10
        max_count_fast_cars = 0
        pack_fast = 0

        for _ in range(count_pack):
            count_fast_car.append(model_bartlet.count_requests())
            temp = count_fast_car[-1]
            if temp > 0:
                pack_fast += 1
            if max_count_fast_cars < temp:
                max_count_fast_cars = temp
        if len(flow_cars) >= 2:
            delta_min_time = min(flow_cars[i][0] - flow_cars[i - 1][0]
                                 for i in range(1, count_pack))
        else:
            delta_min_time = self.time - flow_cars[0][0]

        average_pack_length = delta_min_time / (max_count_fast_cars + c)

        if len(count_fast_car):
            for count_fast, flow in zip(count_fast_car, flow_cars):
                if count_fast == 0:
                    continue
                flow.extend(self._build_pack(
                    average_pack_length, flow[0], count_fast))

        if mode:
            flow_cars = [item for sublist in flow_cars for item in sublist]

        return flow_cars

    def get_time(self):
        return self.time
