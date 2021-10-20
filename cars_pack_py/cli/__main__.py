import matplotlib.pyplot as plt

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice

lamb = 0.5
time = 300
r = 0
g = 0

sd = ServiceDevice()
sd.Start(lamb, time, r, g)
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
