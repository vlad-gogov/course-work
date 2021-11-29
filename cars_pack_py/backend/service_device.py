from .flow import Flow
from .mode_change import ModeChange
from .mode_service_device import ModeServiceDevice
from .type_service import Type
from .car_flow import CarFlow
from .utils import debug_log

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
        time_cycle = 0
        for i in range(len(time_service)):
            time_cycle += time_service[i][0]
            if len(time_service[i]) == 2:
                mods.append(ModeServiceDevice(
                    time_service[i][0], time_service[i][1], Type.DETECTOR_MODE if time_service[i][0] == 0 else None))
            if len(time_service[i]) == 1:
                mods.append(ModeChange(time_service[i][0]))
        for i in range(len(flows)):
            flows[i].add_cars(CarFlow(lamb[i], time_cycle,
                              r[i], g[i]).create_flow(0, mode=True))
        iter = 0
        start_time = 0
        current_flow = None
        delta = 0
        # while flows[0].count <= count_serviced_cars or flows[1].count <= count_serviced_cars:
        while start_time <= time:
            debug_log("Г (", iter + 1, ")", sep="")
            debug_log("Время до обслуживания: ", start_time, "\n")

            current_flow = flows[0] if iter == 0 else flows[1]

            if iter == 0:
                for i in range(len(flows)):
                    flows[i].add_cars(CarFlow(lamb[i], time_cycle + delta, r[i], g[i]).create_flow(
                        start_time + time_cycle, mode=True))

            if mods[iter].get_type() != Type.DETECTOR_MODE:
                start_time = mods[iter].service(current_flow, start_time)
            else:
                if flows[0].cars:
                    debug_log(flows[0].cars[0], "-", start_time, "\n")
                    if (flows[0]):
                        delta = flows[0].cars[0] - start_time - \
                            mods[iter + 1].get_time()
                    if delta > 0:
                        start_time = mods[iter].service(
                            current_flow, start_time, delta)
                    else:
                        delta = 0

            iter = (iter + 1) % (len(mods))
            for i in range(len(flows)):
                if (flows[i].get_queue(start_time) >= MAX_QUEUE):
                    return [-1 for i in range(len(flows))]

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
