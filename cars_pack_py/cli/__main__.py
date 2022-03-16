from concurrent.futures.thread import ThreadPoolExecutor


# TODO
# Проверить постановку машин в очередь

from . import utils
from ..backend.car_flow import CarFlow
from ..backend.service_device import ServiceDevice

lamb = [0.3, 0.1]
r = [0.0, 0.0]
g = [0.0, 0.0]
time_service = [[5, 1], [3], [5, 1], [3]]
count_cars = 5000
K = 80

# sd = ServiceDevice(lamb, r, g, time_service)
# prev = sd.Start_Seq(100)

utils.get_grid(lamb, r, g, time_service, count_cars, K, 5,
               "Loop", "cars_pack_py//results//Puasson//Loop")

# temp = CarFlow(lamb[1], time_service[1][0],
#               r[1], g[1]).create_flow(mode=True)
#print(time_service[1][0], temp)


#sd = ServiceDevice(lamb, r, g, time_service)
#prev = sd.Start_Seq(100)
# print(prev)
# utils.while_param(lamb, r, g, time_service, count_cars, K, 5,
#                  "Loop", "cars_pack_py//results//Puasson//Loop")

# with ThreadPoolExecutor(max_workers=5) as executor:
#    executor.map(utils.wrapper, range(5))

# utils.while_param(lamb, r, g, time_service, count_cars, K, 5,
#                  "G5", "cars_pack_py//results//Bartlet//G5")
# lamb = [0.1, 0.1]
# time = 220
# r = [0.1, 0.1]
# g = [0.1, 0.1]
# time_service = [[60, 1], [3], [60, 1], [0, 1], [3]]
#
# sd = ServiceDevice()
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

# isG5 = True
# p = random.uniform(0, 1 - consts.EPSILON)
# lambda_b = lamb[0] / (1 + r[0]/(1 - g[0]))
# flows[0].add_cars(-math.log(1-p)/lambda_b)
