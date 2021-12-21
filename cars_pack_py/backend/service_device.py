from . import consts
from .flow import Flow
from .mode_change import ModeChange
from .mode_service_device import ModeServiceDevice
from .type_service import Type
from .car_flow import CarFlow
from .utils import debug_log

import math
import random

MAX_QUEUE = 1000
EPSILON_TIME = 1
EPSILON_DISPERSION = 1


class ServiceDevice():
    def __init__(self, lamb: list, r: list, g: list, time_service: list) -> None:
        self.lamb = lamb
        self.r = r
        self.g = g
        self.time_service = time_service

    def Start(self, count_serviced_cars: int) -> list:
        count_flow = len(self.lamb)
        flows = []
        for i in range(count_flow):
            flows.append(Flow())

        mods = []
        for i in range(len(self.time_service)):
            if len(self.time_service[i]) == 2:
                mods.append(ModeServiceDevice(
                    self.time_service[i][0], self.time_service[i][1], Type.DETECTOR_MODE if self.time_service[i][0] == 0 else Type.SERVICE_MODE))
            if len(self.time_service[i]) == 1:
                mods.append(ModeChange(self.time_service[i][0]))

        iter = 1  # Начинаем работу с режима Г(2)
        start_time = 0
        delta = 0
        current_flow = None
        isG5 = False
        time_pi2 = self.time_service[0][0] + \
            self.time_service[1][0] + self.time_service[4][0]
        time_pi1 = self.time_service[1][0] + self.time_service[2][0]

        flows[1].add_cars(self.time_service[1][0])

        while flows[0].count <= count_serviced_cars or flows[1].count <= count_serviced_cars:
            # while start_time <= time:
            debug_log("Г (", iter + 1, ")", sep="")
            debug_log(flows[0].cars, "\n", flows[1].cars)
            debug_log("Время до обслуживания: ", start_time, "\n")

            current_flow = flows[0] if iter == 0 else flows[1]

            if iter == 1:
                if flows[0].queue > 0:
                    isG5 = False
                    flows[0].add_cars(time_pi1 + self.time_service[4][0])
                else:
                    flows[0].add_cars(time_pi1)
            elif iter == 3:
                flows[1].add_cars(time_pi2)
                if flows[0].queue > 0:
                    flows[0].add_cars(self.time_service[4][0])
                    isG5 = False
                else:
                    isG5 = True
                    p = random.uniform(0, 1 - consts.EPSILON)
                    lambda_b = self.lamb[0] / (1 + self.r[0]/(1 - self.g[0]))
                    delta = -math.log(1-p)/lambda_b
                    flows[0].add_cars([delta + start_time], start_time)
            elif iter == 4:
                if isG5:
                    flows[0].add_cars(self.time_service[4][0])

            if mods[iter].get_type() == Type.DETECTOR_MODE and isG5:
                start_time = mods[iter].service(
                    current_flow, start_time, delta)
                delta = 0
                isG5 = False
            else:
                start_time = mods[iter].service(current_flow, start_time)

            iter = (iter + 1) % (len(mods))
            for i in range(len(flows)):
                if (flows[i].queue >= MAX_QUEUE):
                    return [-1 for _ in range(2 * len(flows))]

        result = []
        for flow in flows:
            result.append(flow.get_gamma())
            result.append(flow.get_dispersion())
        return result

    def Start_Seq(self, count_serviced_cars: int) -> list:
        count_flow = len(self.lamb)
        flows = []
        for i in range(count_flow):
            flows.append(Flow(self.lamb[i], self.r[i], self.g[i]))

        # flows[1].cars = [3, 8, 11.5, 12, 12.9]
        # flows[0].cars = [15, 18, 19, 20, 21]
        mods = []
        for i in range(len(self.time_service)):
            if len(self.time_service[i]) == 2:
                mods.append(ModeServiceDevice(
                    self.time_service[i][0], self.time_service[i][1], Type.DETECTOR_MODE if self.time_service[i][0] == 0 else Type.SERVICE_MODE))
            if len(self.time_service[i]) == 1:
                mods.append(ModeChange(self.time_service[i][0]))
        iter = 1  # Начинаем работу с режима Г(2)
        start_time = 0
        current_flow = None

        time_pi2 = self.time_service[0][0] + \
            self.time_service[1][0] + self.time_service[3][0]
        time_pi1 = self.time_service[1][0] + \
            self.time_service[2][0] + self.time_service[3][0]

        flows[1].add_cars(self.time_service[1][0])
        isQueue = False
        while flows[0].count <= count_serviced_cars or flows[1].count <= count_serviced_cars:
            # while start_time <= time:
            debug_log("Г (", iter + 1, ")", sep="")
            debug_log(flows[0].cars, "\n", flows[1].cars)
            debug_log("Время до обслуживания: ", start_time, "\n")

            current_flow = flows[0] if iter == 0 else flows[1]

            if iter == 1:
                flows[0].add_cars(time_pi1)
                if flows[0].get_queue(start_time) >= MAX_QUEUE:
                    isQueue = True
            elif iter == 3:
                flows[1].add_cars(time_pi2)
                if flows[1].get_queue(start_time) >= MAX_QUEUE:
                    isQueue = True

            start_time = mods[iter].service(current_flow, start_time)

            iter = (iter + 1) % (len(mods))
            if isQueue:
                return [-1 for _ in range(2 * len(flows))]

        result = []
        for flow in flows:
            result.append(flow.get_gamma())
            result.append(flow.get_dispersion())
        return result

    def get_weight_avg_gamma(self, gammas: list):
        numerator = 0
        denomerator = 0
        for i in range(len(self.lamb)):
            lamb_b = self.lamb[i] / (1 + self.r[i]/(1 - self.g[i]))
            numerator += lamb_b * gammas[i]
            denomerator += lamb_b
        return numerator / denomerator

    def check_gamma(self, gammas: list):
        for gamma in gammas:
            if gamma == -1:
                return False
        return True
