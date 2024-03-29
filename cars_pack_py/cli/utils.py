import os
import pandas as pd
import numpy as np
import copy

from progress.bar import IncrementalBar

from ..backend import consts
from ..backend.service_device import ServiceDevice
from ..backend.utils import debug_log

from .type_crossroads import TypeCrossroads
from .type_flow import TypeFlow

SEED_TURN = False


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


def create_table(t1: float, t3: float, max_value: list, step: int) -> np.ndarray:
    tabl = np.full((int((max_value[0] - t1) / step) + 2, int((
        max_value[1] - t3) / step) + 2), -1.0, dtype=np.float64)
    for i in range(tabl.shape[0] - 1):
        tabl[tabl.shape[0] - 2 - i][0] = t1 + i * step
    for i in range(tabl.shape[1] - 1):
        tabl[tabl.shape[0] - 1][i + 1] = t3 + i * step
    return tabl


def get_grid(lamb: list, r: list, g: list, time_service: list, count_serviced_cars: int, max_value: list, step: int = 1, path: str = '', opt_value: bool = False, progress_bar: bool = True):
    if not os.path.isdir(path):
        os.mkdir(path)
    name_file = ""
    name_grid = ""
    type_crossroads = TypeCrossroads.LOOP
    type_flow = TypeFlow.PUASSON
    if len(time_service) == 5:
        type_crossroads = TypeCrossroads.G5

    t1 = time_service[0][0]
    t3 = time_service[2][0]

    if t1 > max_value[0] or t3 > max_value[1]:
        print("Введеные неверные максимальные значения")
        return

    temp_path = path

    if type_crossroads == TypeCrossroads.LOOP:
        path += "//Loop"
        if not os.path.isdir(path):
            os.mkdir(path)
        name_grid = "Loop"
    elif type_crossroads == TypeCrossroads.G5:
        path += "//G5"
        if not os.path.isdir(path):
            os.mkdir(path)
        name_grid = "G5"

    if r[0] == 0 and r[1] == 0 and g[0] == 0 and g[1] == 0:
        path += "//Puasson"
        if not os.path.isdir(path):
            os.mkdir(path)
        name_file = f"{name_grid}_{lamb[0]:.{2}}_{lamb[1]:.{2}}_{t1}-{max_value[0]}_{t3}-{max_value[1]}"
    else:
        type_flow = TypeFlow.BARTLETT
        path += f"//Bartlett"
        if not os.path.isdir(path):
            os.mkdir(path)
        path += f"//{r[0]:.{2}}_{g[0]:.{2}} {r[1]:.{2}}_{g[1]:.{2}}"
        if not os.path.isdir(path):
            os.mkdir(path)
        name_file = f"{name_grid}_{lamb[0]:.{2}}_{lamb[1]:.{2}}_{t1}-{max_value[0]}_{t3}-{max_value[1]}"

    sum = 0
    orientation = 0
    for t in time_service:
        sum += t[0]
        if len(t) == 1:
            orientation += t[0]

    tabl_opt = create_table(t1, t3, max_value, step)
    if type_crossroads == TypeCrossroads.G5:
        tabl_frequency_cycle = create_table(t1, t3, max_value, step)
        average_time_G5 = create_table(t1, t3, max_value, step)
        tabl_down_time = create_table(t1, t3, max_value, step)
        tabl_max_G5 = create_table(t1, t3, max_value, step)

    result = np.zeros(len(lamb))

    index_i = tabl_opt.shape[0] - 2
    index_j = 1

    opt_avg = 100000
    opt_t1 = 0
    opt_t3 = 0
    frequence_opt = 0
    average_G5 = 0
    down_G5 = 0
    max_G5 = 0

    if progress_bar:
        bar = IncrementalBar('Countdown', max = (tabl_opt.shape[0] - 1) * (tabl_opt.shape[1] - 1))

    while time_service[2][0] <= max_value[1]:
        while time_service[0][0] <= max_value[0]:
            debug_log("T1 =", time_service[0][0],
                      ", T3 =",  time_service[2][0])
            if SEED_TURN:
                np.random.seed(consts.SEED)
            sd = ServiceDevice(lamb, r, g, time_service)

            if type_crossroads == TypeCrossroads.LOOP:
                result = sd.Start_Seq(count_serviced_cars, type_flow)
                avg = sd.get_weight_avg_gamma([result[0], result[2]])
                debug_log("Y:", avg)
                if avg < opt_avg and avg != -1:
                    opt_avg = avg
                    opt_t1 = time_service[0][0]
                    opt_t3 = time_service[2][0]
                tabl_opt[index_i, index_j] = avg

            elif type_crossroads == TypeCrossroads.G5:
                result = sd.Start_G5(count_serviced_cars, type_flow)
                avg = sd.get_weight_avg_gamma([result[0], result[2]])
                debug_log("Y:", avg)
                if avg < opt_avg and avg != -1:
                    opt_avg = avg
                    opt_t1 = time_service[0][0]
                    opt_t3 = time_service[2][0]
                    frequence_opt = result[4]
                    average_G5 = result[5]
                    down_G5 = result[6]
                    max_G5 = result[7]
                tabl_opt[index_i, index_j] = avg
                tabl_frequency_cycle[index_i, index_j] = result[4]
                average_time_G5[index_i, index_j] = result[5]
                tabl_down_time[index_i, index_j] = result[6]
                tabl_max_G5[index_i, index_j] = result[7]
            debug_log("")
            if progress_bar:
                bar.next()
            if SEED_TURN:
                np.random.seed(0)
            time_service[0][0] += step
            index_i -= 1
        time_service[0][0] = t1
        index_i = tabl_opt.shape[0] - 2
        index_j += 1
        time_service[2][0] += step

    time_service[2][0] = t3
    
    if progress_bar:
        bar.finish()

    if not opt_value:
        pd.DataFrame(tabl_opt).to_csv(
            f"{path}//{name_file}.csv", index=False)
        df = pd.read_csv(f"{path}//{name_file}.csv", sep=',', dtype=np.float64)
        df = df.replace(to_replace=-1, value='', regex=True)
        pd.DataFrame(df).to_csv(
            f"{path}//{name_file}.csv", index=False)
        shift = step
        opt_time_service = time_service.copy()
        opt_time_service[0][0] = opt_t1 - shift if opt_t1 - shift >= 2 else 2
        opt_time_service[2][0] = opt_t3 - shift if opt_t3 - shift >= 2 else 2
        new_max_value = [opt_t1 + shift, opt_t3 + shift]
        get_grid(lamb, r, g, opt_time_service,
                 count_serviced_cars, new_max_value, 1, temp_path, True)
        return

    print(f"Opt value = {opt_avg}; T1 = {opt_t1} T3 = {opt_t3}")
    file = open(f"{name_grid} {r[0]:.{2}}_{g[0]:.{2}} {r[1]:.{2}}_{g[1]:.{2}}.txt", 'a+')
    file.write(f"{lamb[0]:.{2}}_{lamb[1]:.{2}}\n")
    file.write(f"Opt value = {opt_avg}; T1 = {opt_t1} T3 = {opt_t3}\n")
    if type_crossroads == TypeCrossroads.G5:
        print(
            f"Frequency = {frequence_opt}; Average = {average_G5}; Down = {down_G5}; Max = {max_G5}")
        file.write(f"Frequency = {frequence_opt}; Average = {average_G5}; Down = {down_G5}; Max = {max_G5}\n")
    file.write("\n")
    file.close()

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

        pd.DataFrame(tabl_max_G5).to_csv(
            f"{path}//{name_file}_max_G5.csv", index=False)
        df = pd.read_csv(f"{path}//{name_file}_max_G5.csv",
                         sep=',', dtype=np.float64)
        df = df.replace(to_replace=-1, value='',
                        regex=True)
        pd.DataFrame(df).to_csv(
            f"{path}//{name_file}_max_G5.csv", index=False)


def get_state(lamb: list, r: list, g: list, time_service: list, count_serviced_cars: int, max_value: int, step: int = 1, path: str = ''):
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
        name_file = f"{name_grid}_{lamb[0]:.{2}}_{lamb[1]:.{2}}_{t1}-{max_value[0]}_{t3}-{max_value[1]}"
    else:
        path += "//Bartlett//State"
        name_file = f"{name_grid}_{lamb[0]:.{2}}_{r[0]:.{2}}_{g[0]:.{2}}_{lamb[1]:.{2}}_{r[1]:.{2}}_{g[1]:.{2}}_{t1}-{max_value[0]}_{t3}-{max_value[1]}"

    sum = 0
    orientation = 0
    for t in time_service:
        sum += t[0]
        if len(t) == 1:
            orientation += t[0]

    tabl = create_table(t1, t3, max_value, step)

    index_i = tabl.shape[0] - 2
    index_j = 1

    while time_service[2][0] <= max_value[1]:
        while time_service[0][0] <= max_value[0]:
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
    if (lamb[0] >= 0.6):
        return
    while(lamb[0] <= 0.3):
        while(lamb[1] <= 0.5):
            print(f"Progress {lamb[0]:.{2}} {lamb[1]:.{2}}")
            get_grid(lamb, r, g, time_service, count_cars, 5,
                     "Loop", "cars_pack_py//results//Puasson//Loop")
            lamb[1] += 0.1
        lamb[1] = 0.1
        lamb[0] += 0.1


def while_param(lamb: list, r: list, g: list, time_service: list, count_serviced_cars: int, max_value: int, step: int = 1, path: str = ''):
    while(lamb[0] <= 0.3):
        while(lamb[1] <= 0.5):
            print(f"Progress: {lamb[0]:.{2}} {lamb[1]:.{2}}")
            current_time = copy.deepcopy(time_service)
            get_grid(lamb, r, g, current_time,
                     count_serviced_cars, max_value, step, path, False)
            lamb[1] += 0.1
        lamb[0] = round(lamb[0] + 0.1, 2)
        lamb[1] = round(lamb[0] + 0.1, 2)
