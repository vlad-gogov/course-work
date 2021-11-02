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
        #flows[0].add_cars([1, 3, 9, 9.5, 11, 24])
        flows[0].add_cars([7.9, 8.1, 8.5, 9.1, 9.7])
        flows[1].add_cars([3, 4, 7, 8, 11, 19])
        mods = []
        mods.append(ModeServiceDevice(10, 2))
        mods.append(ModeChange(3))
        mods.append(ModeServiceDevice(10, 2))
        mods.append(ModeServiceDevice(10, 2, Type.DETECTOR_MODE))
        mods.append(ModeChange(3))
        iter = 0
        start_time = 0
        current_flow = None
        while start_time < time:
            print("Г (", iter + 1, ")", sep="")
            if iter == 0:
                current_flow = flows[0]
            elif iter == 2 or iter == 3:
                current_flow = flows[1]
            if mods[iter].get_type() != Type.DETECTOR_MODE:
                start_time = mods[iter].service(current_flow, start_time)
            else:
                if flows[0].cars:
                    print(flows[0].cars[0], "-", start_time)
                    delta = flows[0].cars[0] - start_time
                    if delta > 0:
                        start_time = mods[iter].service(
                            current_flow, start_time, delta)
            print()
            iter = (iter + 1) % (len(mods))

        print(flows[0].y)
        print(flows[0].get_gamma(), flows[1].get_gamma())
