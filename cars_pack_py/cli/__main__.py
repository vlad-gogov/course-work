from . import utils

lamb = [0.3, 0.3]
r = [0.4, 0.4]
g = [0.9, 0.9]
#time_service = [[5, 1], [2], [5, 1], [2]]
time_service = [[5, 1], [2], [5, 1], [0, 1], [2]]
count_cars = 5000
K = 270
path = "cars_pack_py//results"
step = 5
max_value = [90, 90]

utils.while_param(lamb, r, g, time_service,
                  count_cars, K, max_value, step, path)

# utils.get_grid(lamb, r, g, time_service,
#                count_cars, K, max_value, step, path, True)

# utils.get_state(lamb, r, g, time_service, count_cars, K,
#                 step, "Correct_Puasson", path + "//Loop//Puasson")
