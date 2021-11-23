from .flow import Flow
from .mode_change import ModeChange
from .mode_service_device import ModeServiceDevice
from .type_service import Type
from .car_flow import CarFlow

# Нарисовать
#flows[0].add_cars([1, 4, 7, 9, 27])
#flows[1].add_cars([1, 3, 5, 11])

MAX_QUEUE = 1000


class ServiceDevice():
    def __init__(self) -> None:
        pass

    def Start(self, lamb: list, time: list, r: list, g: list, time_service: list, count_serviced_cars: int) -> list:
        count_flow = len(lamb)
        flows = []
        models = []
        for i in range(count_flow):
            flows.append(Flow())
            models.append(CarFlow(lamb[i], time, r[i], g[i]))
            # flows[i].add_cars(models[i].create_flow(mode=True))
        #flows[0].add_cars([1, 3, 9, 9.5, 11, 24])
        #flows[0].add_cars([7.9, 8.1, 8.5, 9.1, 9.7])
        #flows[1].add_cars([3, 4, 7, 8, 11, 19])
        #flows[0].add_cars([1, 2, 4, 5, 6, 7])
        #flows[0].add_cars([1, 4, 7, 9, 27])
        #flows[1].add_cars([1, 3, 5, 11, 13, 15])
        mods = []
        time_cycle = 0
        for i in range(len(time_service)):
            time_cycle += time_service[i][0]
            if len(time_service[i]) == 2:
                mods.append(ModeServiceDevice(
                    time_service[i][0], time_service[i][1], Type.DETECTOR_MODE if time_service[i][0] == 0 else None))
            if len(time_service[i]) == 1:
                mods.append(ModeChange(time_service[i][0]))
        iter = 0
        start_time = 0
        current_flow = None
        delta = 0
        while flows[0].count + flows[1].count <= count_serviced_cars:
            #print("Г (", iter + 1, ")", sep="")
            #print("Время до обслуживания: ", start_time)
            # print()
            current_flow = flows[0] if iter == 0 else flows[1]
            if iter == 0:
                for i in range(len(flows)):
                    flows[i].add_cars(models[i].create_flow(
                        start_time, time_cycle + delta, True))

            if mods[iter].get_type() != Type.DETECTOR_MODE:
                start_time = mods[iter].service(current_flow, start_time)
            else:
                if flows[0].cars:
                    #print(flows[0].cars[0], "-", start_time)
                    if (flows[0]):
                        delta = flows[0].cars[0] - start_time - \
                            mods[iter + 1].get_time()
                    if delta > 0:
                        start_time = mods[iter].service(
                            current_flow, start_time, delta)
                    else:
                        delta = 0
            # print()
            #print("Время после обслуживания: ", start_time)
            # print()
            iter = (iter + 1) % (len(mods))
            for i in range(len(flows)):
                if (flows[i].get_queue(start_time) >= MAX_QUEUE):
                    return [-1 for i in range(len(flows))]

        result = []
        for flow in flows:
            result.append(flow.get_gamma())
        return result
