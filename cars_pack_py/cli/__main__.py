import matplotlib.pyplot as plt

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice

lamb = [0.5, 0.3]
time = 40
r = [0.5, 0.2]
g = [0.3, 0.1]
time_service = [[10, 2], [3], [10, 2], [10, 2], [3]]

sd = ServiceDevice()
sd.Start(lamb, time, r, g, time_service)
#flow = CarFlow(lamb, time, r, g)
#temp = flow.create_flow(10)
# print(temp)
#temp_flat = []
# for pack in temp:
#   temp_flat.extend(pack)

#plt.plot(temp_flat, [1] * len(temp_flat), 'ro')
#print(1 + r / (1 - g))
# print(utils.averageLengthPack(temp))
# plt.show()
