from concurrent.futures.thread import ThreadPoolExecutor
import numpy

from cars_pack_py.backend.model_bartlet import ModelBartlet

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice
from .type_crossroads import TypeCrossroads

lamb = [0.1, 0.3]
r = [0.0, 0.0]
g = [0.0, 0.0]
#time_service = [[16, 2], [2], [16, 2], [2]]
time_service = [[10, 2], [2], [16, 2], [0, 2], [2]]
count_cars = 5000
K = 250
path = "cars_pack_py//results"
step = 1
max_value = [20, 33]

# utils.get_grid(lamb, r, g, time_service,
#               count_cars, K, max_value, step, path)

#utils.get_grid(lamb, r, g, time_service, count_cars, K, max_value, step, path)

# utils.get_state(lamb, r, g, time_service, count_cars, K,
#                step, "Correct_Puasson", path + "//Loop//Puasson")
