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
        #model = ModelPoisson(lambda_b, self.time)
        #all_count_requests += model.count_requests()
        #full_time += self.time
        # while not model._is_correct(all_count_requests, full_time):
        #    all_count_requests += model.count_requests()
        #    full_time += self.time
        #self.time = full_time
        all_count_requests = numpy.random.poisson(lambda_b * self.time)
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
        flow_cars = [[car] for car in slow_cars]
        count_pack = len(slow_cars)

        # Fast cars
        c = 2
        model_bartlet = ModelBartlet(self.r, self.g)
        r_stat = self.r
        average_pack_length = 0
        expected_value = model_bartlet.get_expected_value()
        expected_value_stat = expected_value
        lambda_bartlet = self.lamb * expected_value
        lambda_bartlet_stat = lambda_bartlet

        count_fast_car = []

        while abs(r_stat - self.r) < 0.1 * self.r and \
                abs(expected_value_stat - expected_value) < 0.1 * expected_value and \
                abs(lambda_bartlet_stat - lambda_bartlet) < 0.1 * lambda_bartlet:
            count_fast_car.clear()
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
                delta_min_time = 0

            average_pack_length = delta_min_time / (max_count_fast_cars + c)
            r_stat = pack_fast / count_pack
            expected_value_stat = model_bartlet.get_expected_value_custom(
                r_stat, average_pack_length)
            lambda_bartlet_stat = self.lamb * expected_value_stat

        if mode:
            flow_cars = [item for sublist in flow_cars for item in sublist]

        return flow_cars

    def get_time(self):
        return self.time
