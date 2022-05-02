import csv
import os
import glob
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from ..backend.service_device import ServiceDevice
from .type_crossroads import TypeCrossroads

DEBUG = False


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


def create_table(t1: float, t3: float, max_value: list, step: int) -> np.ndarray:
    tabl = np.full((int((max_value[0] - t1) / step) + 2, int((
        max_value[1] - t3) / step) + 2), -1.0, dtype=np.float64)
    for i in range(tabl.shape[0] - 1):
        tabl[tabl.shape[0] - 2 - i][0] = t1 + i * step
    for i in range(tabl.shape[1] - 1):
        tabl[tabl.shape[0] - 1][i + 1] = t3 + i * step
    return tabl


def get_grid(lamb: list, r: list, g: list, time_service: list, count_serviced_cars: int, K: int, max_value: list, step: int = 1, path: str = ''):

    name_file = ""
    name_grid = ""
    type_crossroads = TypeCrossroads.LOOP
    if len(time_service) == 5:
        type_crossroads = TypeCrossroads.G5

    t1 = time_service[0][0]
    t3 = time_service[2][0]

    if type_crossroads == TypeCrossroads.LOOP:
        path += "//Loop"
        name_grid = "Loop"
    elif type_crossroads == TypeCrossroads.G5:
        path += "//G5"
        name_grid = "G5"

    if r[0] == 0 and r[1] == 0 and g[0] == 0 and g[1] == 0:
        path += "//Puasson"
        name_file = f"{name_grid}_{K}_{lamb[0]:.{1}}_{lamb[1]:.{1}}_{t1}_{max_value}"
    else:
        path += "//Bartlett"
        name_file = f"{name_grid}_{K}_{lamb[0]:.{1}}_{r[0]:.{1}}_{g[0]:.{1}}_{lamb[1]:.{1}}_{r[1]:.{1}}_{g[1]:.{1}}_{t1}_{max_value}"

    sum = 0
    orientation = 0
    for t in time_service:
        sum += t[0]
        if len(t) == 1:
            orientation += t[0]

    if sum > K:
        print("Некоректное значение K")
        return

    tabl_opt = create_table(t1, t3, max_value, step)
    if type_crossroads == TypeCrossroads.G5:
        tabl_frequency_cycle = create_table(t1, t3, max_value, step)
        average_time_G5 = create_table(t1, t3, max_value, step)
        tabl_down_time = create_table(t1, t3, max_value, step)

    debug_log(tabl_opt.shape)

    result = np.zeros(len(lamb))

    index_i = tabl_opt.shape[0] - 2
    index_j = 1

    while time_service[0][0] + time_service[2][0] + orientation <= K and time_service[2][0] <= max_value[1]:
        while time_service[0][0] + time_service[2][0] + orientation <= K and time_service[0][0] <= max_value[0]:
            debug_log("T1 =", time_service[0][0],
                      ", T3 =",  time_service[2][0])

            sd = ServiceDevice(lamb, r, g, time_service)

            if type_crossroads == TypeCrossroads.LOOP:
                result = sd.Start_Seq(count_serviced_cars)
                avg = sd.get_weight_avg_gamma([result[0], result[2]])
                debug_log("Y:", avg)
                tabl_opt[index_i, index_j] = avg

            elif type_crossroads == TypeCrossroads.G5:
                result = sd.Start_G5(count_serviced_cars)
                avg = sd.get_weight_avg_gamma([result[0], result[2]])
                debug_log("Y:", avg)
                tabl_opt[index_i, index_j] = avg
                tabl_frequency_cycle[index_i, index_j] = result[4]
                average_time_G5[index_i, index_j] = result[5]
                tabl_down_time[index_i, index_j] = result[6]
            debug_log("")

            time_service[0][0] += step
            index_i -= 1
        time_service[0][0] = t1
        index_i = tabl_opt.shape[0] - 2
        index_j += 1
        time_service[2][0] += step

    time_service[2][0] = t3

    pd.DataFrame(tabl_opt).to_csv(
        f"{path}//{name_file}.csv", index=False)
    df = pd.read_csv(f"{path}//{name_file}.csv", sep=',', dtype=np.float64)
    df = df.replace(to_replace=-1, value='', regex=True)
    pd.DataFrame(df).to_csv(
        f"{path}//{name_file}.csv", index=False)

    if type_crossroads == TypeCrossroads.G5:

        pd.DataFrame(tabl_frequency_cycle).to_csv(
            f"{path}//{name_file}_frequency_cycle.csv", index=False)
        df = pd.read_csv(
            f"{path}//{name_file}_frequency_cycle.csv", sep=',', dtype=np.float64)
        df = df.replace(to_replace=-1, value='', regex=True)
        pd.DataFrame(df).to_csv(
            f"{path}//{name_file}_frequency_cycle.csv", index=False)

        pd.DataFrame(average_time_G5).to_csv(
            f"{path}//{name_file}_average_time_G5.csv", index=False)
        df = pd.read_csv(
            f"{path}//{name_file}_average_time_G5.csv", sep=',', dtype=np.float64)
        df = df.replace(to_replace=-1, value='', regex=True)
        pd.DataFrame(df).to_csv(
            f"{path}//{name_file}_average_time_G5.csv", index=False)

        pd.DataFrame(tabl_down_time).to_csv(
            f"{path}//{name_file}_down_time.csv", index=False)
        df = pd.read_csv(f"{path}//{name_file}_down_time.csv",
                         sep=',', dtype=np.float64)
        df = df.replace(to_replace=-1, value='',
                        regex=True)
        pd.DataFrame(df).to_csv(
            f"{path}//{name_file}_down_time.csv", index=False)


def get_state(lamb: list, r: list, g: list, time_service: list, count_serviced_cars: int, K: int, max_value: int, step: int = 1, path: str = ''):
    name_file = ""
    name_grid = ""
    type_crossroads = TypeCrossroads.LOOP
    if len(time_service) == 5:
        type_crossroads = TypeCrossroads.G5

    t1 = time_service[0][0]
    t3 = time_service[2][0]

    if type_crossroads == TypeCrossroads.LOOP:
        path += "//Loop"
        name_grid = "Loop"
    elif type_crossroads == TypeCrossroads.G5:
        path += "//G5"
        name_grid = "G5"

    if r[0] == 0 and r[1] == 0 and g[0] == 0 and g[1] == 0:
        path += "//Puasson//State"
        name_file = f"{name_grid}_{K}_{lamb[0]:.{1}}_{lamb[1]:.{1}}_{t1}_{max_value}"
    else:
        path += "//Bartlett//State"
        name_file = f"{name_grid}_{K}_{lamb[0]:.{1}}_{r[0]:.{1}}_{g[0]:.{1}}_{lamb[1]:.{1}}_{r[1]:.{1}}_{g[1]:.{1}}_{t1}_{max_value}"

    sum = 0
    orientation = 0
    for t in time_service:
        sum += t[0]
        if len(t) == 1:
            orientation += t[0]

    if sum > K:
        print("Некоректное значение K")
        return

    tabl = create_table(t1, t3, max_value, step)

    index_i = tabl.shape[0] - 2
    index_j = 1

    while time_service[0][0] + time_service[2][0] + orientation <= K and time_service[2][0] <= max_value[1]:
        while time_service[0][0] + time_service[2][0] + orientation <= K and time_service[0][0] <= max_value[0]:
            pi1 = lamb[0]*(time_service[0][0] + time_service[1]
                           [0] + time_service[2][0] + time_service[3][0]) - 1 / time_service[0][1] * time_service[0][0] <= 0
            pi2 = lamb[1]*(time_service[0][0] + time_service[1]
                           [0] + time_service[2][0] + time_service[3][0]) - 1 / time_service[2][1] * time_service[2][0] <= 0
            res = pi1 and pi2
            tabl[index_i, index_j] = 1 if res else -1
            time_service[0][0] += step
            index_i -= 1
        time_service[0][0] = t1
        index_i = tabl.shape[0] - 2
        index_j += 1
        time_service[2][0] += step

    time_service[2][0] = t3

    pd.DataFrame(tabl).to_csv(
        f"{path}//{name_file}.csv", index=False)
    df = pd.read_csv(f"{path}//{name_file}.csv", sep=',', dtype=np.float64)
    df = df.replace(to_replace=-1, value='', regex=True)
    pd.DataFrame(df).to_csv(
        f"{path}//{name_file}.csv", index=False)


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


def while_param(lamb: list, r: list, g: list, time_service: list, count_serviced_cars: int, K: int, max_value: int, step: int = 1, path: str = ''):
    while(lamb[0] <= 0.4):
        while(lamb[1] <= 0.5):
            current_time = time_service.copy()
            get_grid(lamb, r, g, time_service,
                     count_serviced_cars, K, max_value, step, path)
            print(f"Progress: {lamb[0]:.{1}} {lamb[1]:.{1}}")
            lamb[1] += 0.1
        lamb[0] += 0.1
        lamb[1] = lamb[0]
