from .flow import Flow
from .mode_change import ModeChange
from .mode_service_device import ModeServiceDevice
from .type_service import Type
from .car_flow import CarFlow


class ServiceDevice():
    def __init__(self) -> None:
        pass

    def Start(self, lamb: list, time: list, r: list, g: list) -> None:
        count_flow = len(lamb)
        flows = []
        models = []
        for i in range(count_flow):
            flows.append(Flow())
            models.append(CarFlow(lamb[i], time, r[i], g[i]))
            # flows[i].addCars(models[i].create_flow())
        flows[0].add_cars([[1], [3], [4.5, 5], [7], [9]])
        flows[1].add_cars([[3], [4], [7], [8]])
        mods = []
        mods.append(ModeServiceDevice(10, 2))
        mods.append(ModeChange(3))
        mods.append(ModeServiceDevice(10, 2))
        mods.append(ModeChange(3))
        #mods.append(ModeServiceDevice(10, 2, Type.DETECTOR_MODE))
        iter = 0
        start_time = 0
        while start_time < time:
            print("Iter: ", iter)
            current_flow = None
            if iter == 0:
                current_flow = flows[0]
            if iter == 2:
                current_flow = flows[1]

            start_time = mods[iter].service(current_flow, start_time)
            iter = (iter + 1) % (len(mods) - 1)

        print(flows[0].y)
        print(flows[0].get_gamma(), flows[1].get_gamma())
