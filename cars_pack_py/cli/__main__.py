from concurrent.futures.thread import ThreadPoolExecutor


# TODO
# Спросить про зависимость количества максимальной очереди

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice
from .type_crossroads import TypeCrossroads

lamb = [0.1, 0.1]
r = [0.5, 0.7]
g = [0.5, 0.7]
time_service = [[5, 1], [3], [5, 1], [3]]
count_cars = 5000
K = 80

# utils.get_grid(TypeCrossroads.LOOP, lamb, r, g, time_service,
#                count_cars, K, 5, "cars_pack_py//results")

utils.while_param(TypeCrossroads.LOOP, lamb, r, g, time_service,
                  count_cars, K, 5, "cars_pack_py//results")
