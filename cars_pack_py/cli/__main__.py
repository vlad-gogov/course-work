from concurrent.futures.thread import ThreadPoolExecutor
import numpy

# TODO
# Спросить про зависимость количества максимальной очереди

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice
from .type_crossroads import TypeCrossroads

lamb = [0.4, 0.1]
r = [0.5, 0.7]
g = [0.5, 0.7]
time_service = [[20, 3], [3], [20, 2], [0, 3], [3]]
count_cars = 5000
K = 100
path = "cars_pack_py//results"
step = 5

# print(numpy.random.poisson(0.3 * 300))
# print(numpy.random.poisson(0.3 * 500))

utils.get_grid(lamb, r, g, time_service, count_cars, K, step, path)
#utils.while_param(lamb, r, g, time_service, count_cars, K, step, path)
