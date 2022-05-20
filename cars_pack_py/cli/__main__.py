from . import utils

lamb = [0.1, 0.3]
r = [0.6, 0.6]
g = [0.85, 0.85]
#time_service = [[25, 1], [2], [34, 1], [2]]
time_service = [[2, 1], [2], [2, 1], [0, 1], [2]]
count_cars = 5000
K = 270
path = "cars_pack_py//results"
step = 1
max_value = [10, 10]

# utils.while_param(lamb, r, g, time_service,
#                   count_cars, K, max_value, step, path)

utils.get_grid(lamb, r, g, time_service,
               count_cars, K, max_value, step, path, True)

# utils.get_state(lamb, r, g, time_service, count_cars, K,
#                 step, "Correct_Puasson", path + "//Loop//Puasson")
