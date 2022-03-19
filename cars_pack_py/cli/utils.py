import csv
import os
import glob
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from ..backend.service_device import ServiceDevice
from .type_crossroads import TypeCrossroads

EPSILON_TIME = 1
EPSILON_DISPERSION = 1

DEBUG = True


def debug_log(*args, **kwargs):
    pass


if DEBUG:
    def debug_log(*args, **kwargs):
        print(*args, **kwargs)


def averageLengthPack(car_flow: list) -> float:
    dist = 0
    for x in car_flow:
        dist += len(x)
    return dist / len(car_flow)


def expected_value(r: list, g: list) -> list:
    result = []
    for i in range(len(r)):
        result.append(1 + r[i]/(1 - g[i]))
    return result


def combine_csv():
    os.chdir("cars_pack_py//results//")

    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv("test.csv",
                        index=False, encoding='utf-8')


def get_grid(lamb: list, r: list, g: list, time_service: list, count_serviced_cars: int, K: int, step: int = 1, path: str = ''):

    name_file = ""
    name_grid = ""
    type_crossroads = TypeCrossroads.LOOP
    if len(time_service) == 5:
        type_crossroads = TypeCrossroads.G5

    if type_crossroads == TypeCrossroads.LOOP:
        path += "//Loop"
        name_grid = "Loop"
    elif type_crossroads == TypeCrossroads.G5:
        path += "//G5"
        name_grid = "G5"

    if r[0] == 0 and r[1] == 0 and g[0] == 0 and g[1] == 0:
        path += "//Puasson"
        name_file = f"{name_grid}_{K}_{lamb[0]:.{1}}_{lamb[1]:.{1}}"
    else:
        path += "//Bartlett"
        name_file = f"{name_grid}_{K}_{lamb[0]:.{1}}_{r[0]:.{1}}_{g[0]:.{1}}_{lamb[1]:.{1}}_{r[1]:.{1}}_{g[1]:.{1}}"

    sum = 0
    orientation = 0
    for t in time_service:
        sum += t[0]
        if len(t) == 1:
            orientation += t[0]

    if sum > K:
        print("Некоректное значение K")
        return

    final = True

    t1 = time_service[0][0]
    t3 = time_service[2][0]

    tabl = np.zeros((int((K - sum) / step) + 2, int(
        (K - sum) / step) + 2))

    for i in range(tabl.shape[0] - 1):
        tabl[tabl.shape[0] - 2 - i][0] = time_service[0][0] + i * step
        tabl[tabl.shape[0] - 1][i + 1] = time_service[2][0] + i * step

    debug_log(tabl.shape)

    result = np.zeros(len(lamb))

    index_i = tabl.shape[0] - 2
    index_j = 1
    tabl[index_i + 1, index_j - 1] = 0

    while time_service[0][0] + time_service[2][0] + orientation <= K:
        while time_service[0][0] + time_service[2][0] + orientation <= K:
            debug_log("T1 =", time_service[0][0],
                      ", T3 =",  time_service[2][0])
            b = count_serviced_cars
            sd = ServiceDevice(lamb, r, g, time_service)
            over_queue = False
            prev = []
            if type_crossroads == TypeCrossroads.LOOP:
                prev = sd.Start_Seq(b)
            elif type_crossroads == TypeCrossroads.G5:
                prev = sd.Start_G5(b)
            if prev[0] == -1 or prev[2] == -1:
                tabl[index_i, index_j] = -1
                over_queue = True
                break
            while final:
                result = []
                if type_crossroads == TypeCrossroads.LOOP:
                    result = sd.Start_Seq(b)
                elif type_crossroads == TypeCrossroads.G5:
                    result = sd.Start_G5(b)
                debug_log("Count cars:", b)
                debug_log(prev)
                debug_log(result)
                if result[0] == -1 or result[2] == -1:
                    tabl[index_i, index_j] = -1
                    over_queue = True
                    break
                if abs(result[0] - prev[0]) <= EPSILON_TIME and abs(result[2] - prev[2]) <= EPSILON_TIME and abs(result[1] - prev[1]) <= 0.1 * prev[1] and abs(result[3] - prev[3]) <= 0.1 * prev[3]:
                    avg = sd.get_weight_avg_gamma([result[0], result[2]])
                    debug_log("Y:", avg, "\n")
                    tabl[index_i, index_j] = avg
                    final = False
                b += count_serviced_cars
                prev = result
            if over_queue:
                over_queue = False
                break
            time_service[0][0] += step
            index_i -= 1
            final = True
        time_service[0][0] = t1
        index_i = tabl.shape[0] - 2
        index_j += 1
        time_service[2][0] += step

    time_service[2][0] = t3

    pd.DataFrame(tabl).to_csv(
        f"{path}//{name_file}.csv", index=False)


def get_state(lamb: list, r: list, g: list, time_service: list, count_serviced_cars: int, K: int, step: int = 1, name_grid: str = '', path: str = ''):

    sum = 0
    orientation = 0
    for t in time_service:
        sum += t[0]
        if len(t) == 1:
            orientation += t[0]

    if sum > K:
        print("Некоректное значение K")
        return

    t1 = time_service[0][0]
    t3 = time_service[2][0]

    tabl = np.zeros((int((K - sum) / step) + 2, int(
        (K - sum) / step) + 2))

    for i in range(tabl.shape[0] - 1):
        tabl[tabl.shape[0] - 2 - i][0] = time_service[0][0] + i * step
        tabl[tabl.shape[0] - 1][i + 1] = time_service[2][0] + i * step

    index_i = tabl.shape[0] - 2
    index_j = 1
    tabl[index_i + 1, index_j - 1] = 0

    while time_service[0][0] + time_service[2][0] + orientation <= K:
        while time_service[0][0] + time_service[2][0] + orientation <= K:
            pi1 = lamb[0]*(time_service[0][0] + time_service[1]
                           [0] + time_service[2][0] + time_service[3][0]) - 1 / time_service[0][1]*time_service[0][0] <= 0
            pi2 = lamb[1]*(time_service[0][0] + time_service[1]
                           [0] + time_service[2][0] + time_service[3][0]) - 1 / time_service[2][1]*time_service[2][0] <= 0
            res = pi1 and pi2
            tabl[index_i, index_j] = 1 if res else -1
            time_service[0][0] += step
            index_i -= 1
            if res == 0:
                break
        time_service[0][0] = t1
        index_i = tabl.shape[0] - 2
        index_j += 1
        time_service[2][0] += step

    time_service[2][0] = t3

    pd.DataFrame(tabl).to_csv(
        f"{path}//{name_grid}_{K}_{lamb[0]:.{1}}_{lamb[1]:.{1}}.csv", index=False)


def wrapper(thread_id: int):
    lamb = [0.1 * (thread_id + 1), 0.1]
    r = [0.0, 0.0]
    g = [0.0, 0.0]
    time_service = [[5, 1], [3], [5, 1], [0, 1], [3]]
    count_cars = 5000
    K = 80
    if (lamb[0] >= 0.6):
        return
    while(lamb[0] <= 0.5):
        while(lamb[1] <= 0.5):
            print(f"Progress {lamb[0]:.{1}} {lamb[1]:.{1}}")
            get_grid(lamb, r, g, time_service, count_cars, K, 5,
                     "Loop", "cars_pack_py//results//Puasson//Loop")
            lamb[1] += 0.1
        lamb[1] = 0.1
        lamb[0] += 0.1


def while_param(lamb: list, r: list, g: list, time_service: list, count_serviced_cars: int, K: int, step: int = 1, path: str = ''):
    while(lamb[0] <= 0.5):
        while(lamb[1] <= 0.5):
            current_time = time_service.copy()
            get_grid(lamb, r, g, current_time,
                     count_serviced_cars, K, step, path)
            print(f"Progress: {lamb[0]:.{1}} {lamb[1]:.{1}}")
            lamb[1] += 0.1
        lamb[1] = 0.1
        lamb[0] += 0.1
