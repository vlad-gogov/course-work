from . import consts
from .flow import Flow
from .mode_change import ModeChange
from .mode_service_device import ModeServiceDevice
from .type_service import Type, ModesSeq, ModesG5
from .utils import debug_log

import math
import random

MAX_QUEUE = 50
EPSILON_TIME = 1
EPSILON_DISPERSION = 1


class ServiceDevice():
    def __init__(self, lamb: list, r: list, g: list, time_service: list) -> None:
        self.lamb = lamb
        self.r = r
        self.g = g
        self.time_service = time_service

    def Start_G5(self, count_serviced_cars: int) -> list:
        time_Gamma_1 = self.time_service[0][0]
        time_Gamma_2 = self.time_service[1][0]
        time_Gamma_3 = self.time_service[2][0]
        time_Gamma_5 = self.time_service[3][0]
        time_Gamma_4 = self.time_service[4][0]
        count_flow = len(self.lamb)
        flows = []
        for i in range(count_flow):
            flows.append(Flow(self.lamb[i], self.r[i], self.g[i]))

        mods = []
        for i in range(len(self.time_service)):
            if len(self.time_service[i]) == 2:
                mods.append(ModeServiceDevice(
                    self.time_service[i][0], self.time_service[i][1], Type.DETECTOR_MODE if self.time_service[i][0] == 0 else Type.SERVICE_MODE))
            if len(self.time_service[i]) == 1:
                mods.append(ModeChange(self.time_service[i][0]))

        iter = ModesG5.Gamma_2  # Начинаем работу с режима Г(2)
        delta = 0
        current_flow = flows[1]
        isG5 = False
        count_G5 = 0

        count_cycle = 0

        all_time_g5 = 0

        time_for_pi2 = time_Gamma_1 + time_Gamma_2 + time_Gamma_4
        time_for_pi1_default = time_Gamma_2 + time_Gamma_3
        time_for_pi1_full = time_for_pi1_default + time_Gamma_4

        isGenPi1Default = False

        max_q = [0, 0]

        start_time = 0
        flows[1].generation_cars(time_for_pi2, start_time)
        start_time = time_for_pi2
        while flows[0].count <= count_serviced_cars or flows[1].count <= count_serviced_cars:
            debug_log("Г (", iter + 1, ")", sep="")
            debug_log("Время до обслуживания: ", start_time, "\n")

            current_flow = flows[0] if iter == ModesG5.Gamma_1 else flows[1]

            if iter == ModesG5.Gamma_2:
                count_cycle += 1
                if flows[0].queue > 0:
                    isG5 = False
                    flows[0].generation_cars(
                        time_for_pi1_full, start_time)
                else:
                    flows[0].generation_cars(time_for_pi1_default, start_time)
                    isGenPi1Default = True
                    if flows[0].queue > 0:
                        isG5 = False
                    else:
                        isG5 = True
                        # Генерирование первой заявки по 1-ому потоку
                        p = random.uniform(0, 1 - consts.EPSILON)
                        lambda_b = self.lamb[0] / \
                            (1 + self.r[0]/(1 - self.g[0]))
                        delta = -math.log(1-p)/lambda_b
                        flows[0].add_cars(delta + start_time)

            elif iter == ModesG5.Gamma_4:
                if isG5 or isGenPi1Default:
                    flows[0].generation_cars(time_Gamma_4, start_time)
                    isG5 = False
                    isGenPi1Default = False
                flows[1].generation_cars(time_for_pi2, start_time)

            for i in range(count_flow):
                if flows[i].queue >= max_q[i]:
                    max_q[i] = flows[i].queue
                if flows[i].queue >= MAX_QUEUE:
                    print("Max queue", max_q)
                    return [-1 for _ in range(2 * len(flows))]

            if mods[iter].get_type() == Type.DETECTOR_MODE and isG5:
                all_time_g5 += delta
                start_time = mods[iter].service(
                    current_flow, start_time, delta)
                delta = 0
                count_G5 += 1
            else:
                start_time = mods[iter].service(current_flow, start_time)

            iter = (iter + 1) % (len(mods))

        result = []
        for flow in flows:
            result.append(flow.get_gamma())
            result.append(flow.get_dispersion())
        # отношение числа срабатывания режима Г5 к числу всех циклов
        result.append(count_G5 / count_cycle)

        # среднее время пребывания в режиме Г5
        result.append(all_time_g5 / count_G5)

        # среднее время простоя режима G5
        result.append(mods[ModesG5.Gamma_5].down_time /
                      count_G5 if count_G5 != 0 else 0)
        print("Max queue", max_q)
        return result

    def Start_Seq(self, count_serviced_cars: int) -> list:
        time_Gamma_1 = self.time_service[0][0]
        time_Gamma_2 = self.time_service[1][0]
        time_Gamma_3 = self.time_service[2][0]
        time_Gamma_4 = self.time_service[3][0]
        count_flow = len(self.lamb)
        flows = []
        for i in range(count_flow):
            flows.append(Flow(self.lamb[i], self.r[i], self.g[i]))

        mods = []
        for i in range(len(self.time_service)):
            if len(self.time_service[i]) == 2:
                mods.append(ModeServiceDevice(
                    self.time_service[i][0], self.time_service[i][1], Type.DETECTOR_MODE if self.time_service[i][0] == 0 else Type.SERVICE_MODE))
            if len(self.time_service[i]) == 1:
                mods.append(ModeChange(self.time_service[i][0]))
        iter = ModesSeq.Gamma_2  # Начинаем работу с режима Г(2)
        current_flow = flows[1]
        isQueue = False

        time_for_pi1 = time_Gamma_2 + time_Gamma_3 + time_Gamma_4
        time_for_pi2 = time_Gamma_1 + time_Gamma_2 + time_Gamma_4

        start_time = 0
        current_flow.generation_cars(time_for_pi2, start_time)
        start_time = time_for_pi2
        while flows[0].count <= count_serviced_cars or flows[1].count <= count_serviced_cars:
            debug_log("Г (", iter + 1, ")", sep="")
            debug_log("Время до обслуживания: ", start_time, "\n")

            current_flow = flows[0] if iter == ModesSeq.Gamma_1 else flows[1]

            if iter == ModesSeq.Gamma_2:
                flows[0].generation_cars(time_for_pi1, start_time)
                if flows[0].queue >= MAX_QUEUE:
                    isQueue = True
            elif iter == ModesSeq.Gamma_4:
                flows[1].generation_cars(time_for_pi2, start_time)
                if flows[1].queue >= MAX_QUEUE:
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
