from . import consts
from .model_poisson import ModelPoisson
from .model_bartlet import ModelBartlet

import random


class CarFlow:
    def __init__(self, lamb: float = 0, time: float = 0, r: float = 0, g: float = 0) -> None:
        self.lamb = lamb
        self.time = time
        self.r = r
        self.g = g

    def _check_distance_pack(self, slow_cars: list) -> list:
        result = [[slow_cars[0]]]
        index_pack = 0
        temp = slow_cars[0]
        for car in slow_cars[1:]:
            if car - temp <= consts.DISTANCE_PACK:
                result[index_pack].append(car)
            else:
                result.append([car])
                index_pack += 1
                temp = car

        return result

    def _create_cars_slow(self) -> list:
        all_count_requests = 0
        full_time = 0
        lambda_b = self.lamb / (1 + self.r/(1 - self.g))
        model = ModelPoisson(lambda_b, self.time)
        all_count_requests += model.count_requests()
        full_time += self.time
        while abs(all_count_requests / full_time - lambda_b) >= 0.1 * lambda_b:
            all_count_requests += model.count_requests()
            full_time += self.time
        self.time = full_time

        slow_cars = [random.uniform(
            0, 1 - consts.EPSILON) * self.time for i in range(all_count_requests)]

        slow_cars.sort()

        return slow_cars

    def _build_pack(self, average_pack_length: float, time_start: float, count_fast_cars: int):
        pack = []
        for _ in range(count_fast_cars):
            time_moment = time_start + \
                random.uniform(0, 1 - consts.EPSILON) * average_pack_length
            while time_moment > self.time:
                time_moment = time_start + \
                    random.uniform(0, 1 - consts.EPSILON) * average_pack_length
            pack.append(time_moment)
        pack.sort()
        return pack

    def create_flow(self, time_start: float = 0) -> list:
        # Slow cars
        slow_cars = self._create_cars_slow()
        flow_cars = self._check_distance_pack(slow_cars)
        count_pack = len(flow_cars)

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

            delta_min_time = min(flow_cars[i][0] - flow_cars[i - 1][0]
                                 for i in range(1, count_pack))

            average_pack_length = delta_min_time / (max_count_fast_cars + c)
            r_stat = pack_fast / count_pack
            expected_value_stat = model_bartlet.get_expected_value_custom(
                r_stat, average_pack_length)
            lambda_bartlet_stat = self.lamb * expected_value_stat

        if count_fast_car:
            for count_fast, flow in zip(count_fast_car, flow_cars):
                if count_fast + 1 == len(flow):
                    continue
                if count_fast + 1 > len(flow):
                    pack = self._build_pack(
                        average_pack_length, flow[0], count_fast - len(flow))
                    flow.extend(pack)
                elif count_fast < len(flow):
                    while count_fast + 1 < len(flow):
                        flow.pop()
        else:
            for flow in flow_cars:
                while len(flow) != 1:
                    flow.pop()

        if time_start != 0:
            for i in range(len(flow_cars)):
                for j in range(len(flow_cars[i])):
                    flow_cars[i][j] += time_start

        return flow_cars
