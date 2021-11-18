import matplotlib.pyplot as plt

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice

lamb = [0.2, 0.2]
time = 100
r = [0.5, 0.5]
g = [0.5, 0.5]
time_service = [[60, 0.5], [3], [45, 0.5], [0, 0.5], [3]]

f = True
count_cars = 5000
sd = ServiceDevice()
prev = sd.Start(lamb, time, r, g, time_service, count_cars)
b = count_cars

while f:
    b += count_cars
    a = sd.Start(lamb, time, r, g, time_service, b)
    if abs(a[0] - prev[0]) <= 1 and abs(a[1] - prev[1]) <= 1:
        f = False
    prev = a
print(b)
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
