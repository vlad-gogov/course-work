import matplotlib.pyplot as plt

from ..backend.car_flow import CarFlow
from . import utils

lamb = 0.5
time = 100
r = 0
g = 0

flow = CarFlow(lamb, time, r, g)
temp = flow.create_flow()
temp_flat = []
for pack in temp:
    temp_flat.extend(pack)

plt.plot(temp_flat, [1] * len(temp_flat), 'ro')
print(1 + r / (1 - g))
print(utils.averageLengthPack(temp))
print(temp)
# plt.show()
