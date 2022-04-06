from concurrent.futures.thread import ThreadPoolExecutor
import numpy

# TODO
# Спросить про зависимость количества максимальной очереди

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice
from .type_crossroads import TypeCrossroads

lamb = [0.1, 0.1]
r = [0.0, 0.0]
g = [0.0, 0.0]
time_service = [[15, 3], [2], [15, 3], [2]]
count_cars = 5000
K = 100
path = "cars_pack_py//results"
step = 5

# print(numpy.random.poisson(0.3 * 300))
# print(numpy.random.poisson(0.3 * 500))

utils.while_param(lamb, r, g, time_service, count_cars, K, step, path)
# utils.get_state(lamb, r, g, time_service, count_cars, K,
#                step, "Correct_Puasson", path + "//Loop//Puasson")
