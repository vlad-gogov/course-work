from concurrent.futures.thread import ThreadPoolExecutor
import numpy
import os

from cars_pack_py.backend.model_bartlet import ModelBartlet

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice
from .type_crossroads import TypeCrossroads

lamb = [0.1, 0.1]
r = [0.7, 0.7]
g = [0.95, 0.95]
#time_service = [[5, 1], [2], [5, 1], [2]]
time_service = [[2, 1], [2], [2, 1], [0, 1], [2]]
count_cars = 5000
K = 270
path = "cars_pack_py//results"
step = 1
max_value = [6, 6]
if not os.path.isdir(path):
    os.mkdir(path)

# utils.while_param(lamb, r, g, time_service,
#                   count_cars, K, max_value, step, path)

utils.get_grid(lamb, r, g, time_service,
               count_cars, K, max_value, step, path, True)

# utils.get_state(lamb, r, g, time_service, count_cars, K,
#                 step, "Correct_Puasson", path + "//Loop//Puasson")
