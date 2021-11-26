import matplotlib.pyplot as plt
import pandas

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice

#lamb = [0.1, 0.1]
#time = 220
#r = [0.1, 0.1]
#g = [0.1, 0.1]
#time_service = [[20, 4], [4], [15, 5], [4]]
#
#sd = ServiceDevice()
#
# a = sd.Start(lamb, time, r, g,
#             time_service, 0)
#print(a[0], a[1])

# utils.Test()
utils.combine_csv()

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
