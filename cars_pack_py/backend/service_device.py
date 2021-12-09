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
    def __init__(self) -> None:
        pass

    def Start(self, lamb: list, time: list, r: list, g: list, time_service: list, count_serviced_cars: int) -> list:
        count_flow = len(lamb)
        flows = []
        for i in range(count_flow):
            flows.append(Flow())

        # flows[0].add_cars([2, 5, 8, 9, 18, 20, 24, 32, 45, 46, 51, 55, 62])
        # flows[1].add_cars([3, 10, 14, 15, 21, 35, 41, 45, 48, 51, 53, 55, 56])

        mods = []
        for i in range(len(time_service)):
            if len(time_service[i]) == 2:
                mods.append(ModeServiceDevice(
                    time_service[i][0], time_service[i][1], Type.DETECTOR_MODE if time_service[i][0] == 0 else Type.DEFAULT_MODE))
            if len(time_service[i]) == 1:
                mods.append(ModeChange(time_service[i][0]))

        iter = 1  # Начинаем работу с режима Г(2)
        start_time = 0
        delta = 0
        current_flow = None
        isG5 = False
        time_pi2 = time_service[0][0] + time_service[1][0] + time_service[4][0]
        time_pi1 = time_service[1][0] + time_service[2][0]

        flows[1].add_cars(CarFlow(lamb[1], time_service[1][0],
                          r[1], g[1]).create_flow(mode=True), start_time)

        while flows[0].count <= count_serviced_cars or flows[1].count <= count_serviced_cars:
            # while start_time <= time:
            debug_log("Г (", iter + 1, ")", sep="")
            debug_log("Время до обслуживания: ", start_time, "\n")

            current_flow = flows[0] if iter == 0 else flows[1]

            if iter == 1:
                if flows[0].queue > 0:
                    isG5 = False
                    flows[0].add_cars(CarFlow(lamb[0], time_pi1 + time_service[4][0],
                                              r[0], g[0]).create_flow(start_time, mode=True), start_time)
                else:
                    flows[0].add_cars(CarFlow(lamb[0], time_pi1,
                                              r[0], g[0]).create_flow(start_time, mode=True), start_time)
            elif iter == 3:
                flows[1].add_cars(CarFlow(lamb[1], time_pi2,
                                          r[1], g[1]).create_flow(start_time, mode=True), start_time)
                if flows[0].queue > 0:
                    flows[0].add_cars(CarFlow(lamb[0], time_service[4][0],
                                              r[0], g[0]).create_flow(start_time, mode=True), start_time)
                    isG5 = False
                else:
                    isG5 = True
                    p = random.uniform(0, 1 - consts.EPSILON)
                    lambda_b = lamb[0] / (1 + r[0]/(1 - g[0]))
                    delta = -math.log(1-p)/lambda_b
                    flows[0].add_cars([delta + start_time], start_time)
            elif iter == 4:
                if isG5:
                    flows[0].add_cars(CarFlow(lamb[0], time_service[4][0],
                                              r[0], g[0]).create_flow(start_time, mode=True), start_time)

            if mods[iter].get_type() == Type.DETECTOR_MODE and isG5:
                start_time = mods[iter].service(
                    current_flow, start_time, delta)  # - mods[iter + 1].get_time()
                delta = 0
                isG5 = False
            else:
                start_time = mods[iter].service(current_flow, start_time)

            iter = (iter + 1) % (len(mods))
            for i in range(len(flows)):
                if (flows[i].queue >= MAX_QUEUE):
                    return [-1 for i in range(2 * len(flows))]

        result = []
        for flow in flows:
            result.append(flow.get_gamma())
            result.append(flow.get_dispersion())
        return result

    def get_weight_avg_gamma(self, lambs: list, gammas: list):
        numerator = 0
        denomerator = 1
        for i in range(len(lambs)):
            numerator += lambs[i] * gammas[i]
            denomerator += lambs[i]
        return numerator / denomerator

    def check_gamma(self, gammas: list):
        for gamma in gammas:
            if gamma == -1:
                return False
        return True
