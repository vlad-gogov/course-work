from concurrent.futures.thread import ThreadPoolExecutor
import numpy

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice
from .type_crossroads import TypeCrossroads

lamb = [0.1, 0.1]
r = [0.5, 0.5]
g = [0.5, 0.5]
time_service = [[15, 2], [2], [15, 2], [0, 2], [2]]
count_cars = 5000
K = 100
path = "cars_pack_py//results"
step = 5

utils.while_param(lamb, r, g, time_service, count_cars, K, step, path)

# utils.get_state(lamb, r, g, time_service, count_cars, K,
#                step, "Correct_Puasson", path + "//Loop//Puasson")
