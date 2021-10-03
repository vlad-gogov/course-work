import matplotlib.pyplot as plt

from ..backend.car_flow import CarFlow

flow = CarFlow(0.5, 100, 0.5, 0.5)
temp = flow.create_flow()
temp_flat = []
for pack in temp:
    temp_flat.extend(pack)

plt.plot(temp_flat, [1] * len(temp_flat), 'ro')
plt.show()
