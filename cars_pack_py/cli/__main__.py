import matplotlib.pyplot as plt
import os

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice

lamb = [0.9, 0.5]
time = 200
r = [0.9, 0.5]
g = [0.9, 0.7]
time_service = [[20, 2], [3], [20, 1], [0, 2], [3]]
count_cars = 5000
K = 50

utils.get_grid(lamb, time, r, g, time_service, count_cars, K)


#lamb = [0.1, 0.1]
#time = 220
#r = [0.1, 0.1]
#g = [0.1, 0.1]
#time_service = [[60, 1], [3], [60, 1], [0, 1], [3]]
#
#sd = ServiceDevice()
#
# a = sd.Start(lamb, time, r, g,
#             time_service, 0)
# print(a)

# utils.Test()
# utils.combine_csv()

# flow = CarFlow(lamb, time, r, g)
# temp = flow.create_flow(10)
# print(temp)
# temp_flat = []
# for pack in temp:
#   temp_flat.extend(pack)

# plt.plot(temp_flat, [1] * len(temp_flat), 'ro')
# print(1 + r / (1 - g))
# print(utils.averageLengthPack(temp))
# plt.show()
