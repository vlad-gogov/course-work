from cars_pack_py.cli.type_flow import TypeFlow
from . import consts
from .flow import Flow
from .mode_change import ModeChange
from .mode_service_device import ModeServiceDevice
from .type_service import Type, ModesSeq, ModesG5
from .utils import debug_log

import numpy
import math

MAX_queue = 1000
EPSILON_TIME = 1
EPSILON_DISPERSION = 1


class ServiceDevice():
    def __init__(self, lamb: list, r: list, g: list, time_service: list) -> None:
        self.lamb = lamb
        self.r = r
        self.g = g
        self.time_service = time_service

    def Start_G5(self, count_serviced_cars: int, type_flow: TypeFlow) -> list:
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
        max_q = [0, 0]
        start_time = 0
        delta = 0
        isG5 = False
        isGenPi1Default = False
        count_G5 = 0
        min_G5 = 10000
        max_G5 = 0
        count_cycle = 0
        all_time_G5 = 0

        time_for_pi2 = time_Gamma_1 + time_Gamma_2 + time_Gamma_4
        time_for_pi1_default = time_Gamma_2 + time_Gamma_3
        time_for_pi1_full = time_for_pi1_default + time_Gamma_4

        current_flow = flows[1]
        flows[1].generation_cars(time_for_pi2, start_time)
        start_time = time_for_pi2

        lambda_b = self.lamb[0] / (1 + self.r[0]/(1 - self.g[0]))

        count_cars = count_serviced_cars
        while flows[0].count <= count_cars or flows[1].count <= count_cars:

            current_flow = flows[0] if iter == ModesG5.Gamma_1 else flows[1]

            if iter == ModesG5.Gamma_1:
                current_flow.generation_cars(
                    mods[iter].get_time(), start_time)
            elif iter == ModesG5.Gamma_2:
                count_cycle += 1
                if flows[0].queue() > 0:
                    isG5 = False
                    flows[0].generation_cars(
                        time_for_pi1_full, start_time)
                else:
                    flows[0].generation_cars(time_for_pi1_default, start_time)
                    isGenPi1Default = True
                    if flows[0].queue() > 0:
                        isG5 = False
                    else:
                        isG5 = True

            elif iter == ModesG5.Gamma_3:
                if isG5:
                    # Генерирование первой заявки по 1-ому потоку
                    while delta <= 0:
                        # p = numpy.random.uniform(
                        #     1 - numpy.exp((start_time + mods[iter].get_time() - flows[0].get_last_slow_cars()) * lambda_b), 1 - consts.EPSILON)
                        p = numpy.random.uniform(0, 1 - consts.EPSILON)
                        time_next_slow_car = -math.log(1-p)/lambda_b
                        delta = time_next_slow_car + \
                            flows[0].get_last_slow_cars() - start_time - \
                            mods[iter].get_time()
                        # print(delta)

                    count_G5 += 1

                    if delta < min_G5 and delta != 0:
                        min_G5 = delta
                    if delta > max_G5:
                        max_G5 = delta

                    flows[0].add_cars(
                        flows[0].get_last_slow_cars() + time_next_slow_car)
                    all_time_G5 += delta

                    flows[1].generation_cars(
                        mods[iter].get_time() + delta, start_time)
                else:
                    flows[1].generation_cars(mods[iter].get_time(), start_time)

            elif iter == ModesG5.Gamma_4:
                if isG5 or isGenPi1Default:
                    flows[0].generation_cars(time_Gamma_4, start_time)
                    isG5 = False
                    isGenPi1Default = False
                flows[1].generation_cars(time_for_pi2, start_time)

            for i in range(count_flow):
                if flows[i].queue() >= MAX_queue:
                    return [-1 for _ in range(6 * len(flows))]

            if iter == ModesG5.Gamma_3 and isG5:
                start_time = mods[iter].service(
                    current_flow, start_time, delta)
                delta = 0
            else:
                start_time = mods[iter].service(current_flow, start_time)

            iter = (iter + 1) % (len(mods))

        prev = []
        for flow in flows:
            prev.append(flow.get_gamma())
            prev.append(flow.get_dispersion())

        finish = False
        next = []
        if type_flow == TypeFlow.BARTLETT:
            count_serviced_cars *= 2
        while(not finish):

            count_cars += count_serviced_cars

            while flows[0].count <= count_cars or flows[1].count <= count_cars:

                current_flow = flows[0] if iter == ModesG5.Gamma_1 else flows[1]

                if iter == ModesG5.Gamma_1:
                    current_flow.generation_cars(
                        mods[iter].get_time(), start_time)
                elif iter == ModesG5.Gamma_2:
                    count_cycle += 1
                    if flows[0].queue() > 0:
                        isG5 = False
                        flows[0].generation_cars(
                            time_for_pi1_full, start_time)
                    else:
                        flows[0].generation_cars(
                            time_for_pi1_default, start_time)
                        isGenPi1Default = True
                        if flows[0].queue() > 0:
                            isG5 = False
                        else:
                            isG5 = True

                elif iter == ModesG5.Gamma_3:
                    if isG5:
                        # Генерирование первой заявки по 1-ому потоку
                        while delta <= 0:
                            # p = numpy.random.uniform(
                            #     1 - numpy.exp((start_time + mods[iter].get_time() - flows[0].get_last_slow_cars()) * lambda_b), 1 - consts.EPSILON)
                            p = numpy.random.uniform(0, 1 - consts.EPSILON)
                            time_next_slow_car = -math.log(1-p)/lambda_b

                            delta = time_next_slow_car + \
                                flows[0].get_last_slow_cars() - start_time - \
                                mods[iter].get_time()

                        count_G5 += 1

                        if delta < min_G5 and delta != 0:
                            min_G5 = delta
                        if delta > max_G5:
                            max_G5 = delta

                        flows[0].add_cars(
                            flows[0].get_last_slow_cars() + time_next_slow_car)
                        all_time_G5 += delta

                        flows[1].generation_cars(
                            mods[iter].get_time() + delta, start_time)
                    else:
                        flows[1].generation_cars(
                            mods[iter].get_time(), start_time)

                elif iter == ModesG5.Gamma_4:
                    if isG5 or isGenPi1Default:
                        flows[0].generation_cars(time_Gamma_4, start_time)
                        isG5 = False
                        isGenPi1Default = False
                    flows[1].generation_cars(time_for_pi2, start_time)

                for i in range(count_flow):
                    if flows[i].queue() >= MAX_queue:
                        return [-1 for _ in range(6 * len(flows))]

                if iter == ModesG5.Gamma_3 and isG5:
                    start_time = mods[iter].service(
                        current_flow, start_time, delta)
                    delta = 0
                else:
                    start_time = mods[iter].service(current_flow, start_time)

                iter = (iter + 1) % (len(mods))

            for flow in flows:
                next.append(flow.get_gamma())
                next.append(flow.get_dispersion())

            debug_log("Count cars:", count_cars)
            debug_log(prev)
            debug_log(next)

            if abs(next[0] - prev[0]) <= EPSILON_TIME and abs(next[2] - prev[2]) <= EPSILON_TIME and abs(next[1] - prev[1]) <= 0.1 * prev[1] and abs(next[3] - prev[3]) <= 0.1 * prev[3]:
                finish = True
            else:
                prev = next.copy()
                next.clear()

        # print(
        #     f"Отношение числа срабатывания режима Г5 к числу всех циклов {count_G5} / {count_cycle}")
        # print(
        #     f"Число обслужанных машин по потокам {flows[0].count} / {flows[1].count}")

        # отношение числа срабатывания режима Г5 к числу всех циклов
        next.append(count_G5 / count_cycle)

        # среднее время пребывания в режиме Г5
        next.append(all_time_G5 / count_G5 if count_G5 != 0 else 0)

        # среднее время простоя режима G5
        next.append(mods[ModesG5.Gamma_3].down_time /
                    count_G5 if count_G5 != 0 else 0)

        # минимальное время пребывания в режиме Г5
        next.append(min_G5 if min_G5 != 10000 else 0)

        # максимальное время пребывания в режиме Г5
        next.append(max_G5)

        return next

    def Start_Seq(self, count_serviced_cars: int, type_flow: TypeFlow) -> list:
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
        time_for_pi1 = time_Gamma_2 + time_Gamma_3 + time_Gamma_4
        time_for_pi2 = time_Gamma_1 + time_Gamma_2 + time_Gamma_4

        count_cars = count_serviced_cars

        max_q = [0, 0]
        iter = ModesSeq.Gamma_2
        start_time = 0
        current_flow = flows[1]
        current_flow.generation_cars(time_for_pi2, start_time)
        start_time = time_for_pi2
        prev = []
        while flows[0].count <= count_cars or flows[1].count <= count_cars:

            current_flow = flows[0] if iter == ModesSeq.Gamma_1 else flows[1]

            if iter == ModesSeq.Gamma_1 or iter == ModesSeq.Gamma_3:
                current_flow.generation_cars(
                    mods[iter].get_time(), start_time)
            elif iter == ModesSeq.Gamma_2:
                flows[0].generation_cars(time_for_pi1, start_time)
            elif iter == ModesSeq.Gamma_4:
                flows[1].generation_cars(time_for_pi2, start_time)

            start_time = mods[iter].service(current_flow, start_time)

            iter = (iter + 1) % (len(mods))

            for i in range(count_flow):
                if flows[i].queue() >= max_q[i]:
                    max_q[i] = flows[i].queue()

            for i in range(count_flow):
                if flows[i].queue() >= max_q[i]:
                    max_q[i] = flows[i].queue()
                if flows[i].queue() >= MAX_queue:
                    return [-1 for _ in range(2 * len(flows))]

        for flow in flows:
            prev.append(flow.get_gamma())
            prev.append(flow.get_dispersion())

        finish = False
        next = []
        if type_flow == TypeFlow.BARTLETT:
            count_serviced_cars *= 2
        while(not finish):

            count_cars += count_serviced_cars

            while flows[0].count <= count_cars or flows[1].count <= count_cars:

                current_flow = flows[0] if iter == ModesSeq.Gamma_1 else flows[1]

                if iter == ModesSeq.Gamma_1 or iter == ModesSeq.Gamma_3:
                    current_flow.generation_cars(
                        mods[iter].get_time(), start_time)
                elif iter == ModesSeq.Gamma_2:
                    flows[0].generation_cars(time_for_pi1, start_time)
                elif iter == ModesSeq.Gamma_4:
                    flows[1].generation_cars(time_for_pi2, start_time)

                start_time = mods[iter].service(current_flow, start_time)

                iter = (iter + 1) % (len(mods))

                for i in range(count_flow):
                    if flows[i].queue() >= max_q[i]:
                        max_q[i] = flows[i].queue()

                for i in range(count_flow):
                    if flows[i].queue() >= max_q[i]:
                        max_q[i] = flows[i].queue()
                    if flows[i].queue() >= MAX_queue:
                        return [-1 for _ in range(2 * len(flows))]

            for flow in flows:
                next.append(flow.get_gamma())
                next.append(flow.get_dispersion())

            debug_log("Count cars:", count_cars)
            debug_log(prev)
            debug_log(next)

            if abs(next[0] - prev[0]) <= EPSILON_TIME and abs(next[2] - prev[2]) <= EPSILON_TIME and abs(next[1] - prev[1]) <= 0.1 * prev[1] and abs(next[3] - prev[3]) <= 0.1 * prev[3]:
                finish = True
            else:
                prev = next.copy()
                next.clear()

        return next

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
