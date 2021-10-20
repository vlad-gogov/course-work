from .flow import Flow
from .mode_change import ModeChange
from .mode_service_device import ModeServiceDevice
from .type_service import Type
from .car_flow import CarFlow


class ServiceDevice():
    def __init__(self) -> None:
        pass

    def Start(self, lamb: float = 0, time: float = 0, r: float = 0, g: float = 0) -> None:
        p1 = Flow()
        p2 = Flow()
        mods = []
        model = CarFlow(lamb, time, r, g)
        mods.append(ModeServiceDevice(10, 2))
        mods.append(ModeChange(3))
        mods.append(ModeServiceDevice(10, 2))
        mods.append(ModeServiceDevice(10, 2, Type.DETECTOR_MODE))
        mods.append(ModeChange(3))
        p1.addCars(model.create_flow())
        p2.addCars(model.create_flow())
        iter = 0
        start_time = 0
        while start_time < time:
            print("Iter: ", iter)
            if mods[iter].getType() == Type.DETECTOR_MODE:
                print("DETECTOR_MODE")
            else:
                print("Default")
            print(start_time)
            start_time = mods[iter].service(p1, start_time)
            iter = 0 if len(mods) - 1 == iter else iter + 1
