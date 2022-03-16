from concurrent.futures.thread import ThreadPoolExecutor


# TODO
# Спросить про зависимость количества максимальной очереди

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice

lamb = [0.1, 0.4]
r = [0.0, 0.0]
g = [0.0, 0.0]
time_service = [[5, 1], [3], [5, 1], [3]]
count_cars = 5000
K = 80

utils.get_grid(lamb, r, g, time_service, count_cars, K, 5,
               "Loop", "cars_pack_py//results//Puasson//Loop")

# utils.while_param(lamb, r, g, time_service, count_cars, K, 5,
#                   "Loop", "cars_pack_py//results//Puasson//Loop")

# utils.while_param(lamb, r, g, time_service, count_cars, K, 5,
#                  "Correct_Loop", "cars_pack_py//results//Puasson//Loop")
