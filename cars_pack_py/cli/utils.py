import csv
import os
import glob
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from ..backend.service_device import ServiceDevice

EPSILON_TIME = 1
EPSILON_DISPERSION = 1


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


def thread_function(thread_id: int):
    asfile = open(
        f"cars_pack_py//results//test_{thread_id}.csv", "w", encoding='utf-8')

    fieldnames = ['#', 'count cars', 'lamb1', 'lamb2', 'r1', 'r2', 'g1', 'g2',
                  'gamma1', 'gamma2', "average length pack 1:", "average length pack 2:"]
    writer = csv.DictWriter(asfile, fieldnames=fieldnames)
    writer.writeheader()

    lamb = [0.1 * (thread_id + 1), 0.1]
    time = 100
    r = [0.1, 0.1]
    g = [0.1, 0.1]
    time_service = [[60, 0.5], [3], [60, 0.5], [0, 0.5], [3]]

    f = True
    count_cars = 5000
    sd = ServiceDevice()
    l = thread_id * (9 ** 5) + 1
    for _ in range(9):
        for _ in range(9):
            for _ in range(9):
                for _ in range(9):
                    for _ in range(9):
                        prev = sd.Start(
                            lamb, time, r, g, time_service, count_cars)
                        b = count_cars
                        while f:
                            b += count_cars
                            a = sd.Start(lamb, time, r, g,
                                         time_service, b)
                            if abs(a[0] - prev[0]) <= 1 and abs(a[1] - prev[1]) <= 1:
                                avglengt = expected_value(r, g)
                                writer.writerow({'#': l, 'count cars': b, 'lamb1': lamb[0], 'r1': r[0], 'g1': g[0],
                                                 'gamma1': a[0], "average length pack 1:": avglengt[0], 'lamb2': lamb[1], 'r2': r[1], 'g2': g[1], 'gamma2': a[1], "average length pack 2:": avglengt[1]})
                                f = False
                            prev = a
                        f = True
                        print(l)
                        l += 1
                        g[1] += 0.1
                    g[1] = 0.1
                    g[0] += 0.1
                g[1] = 0.1
                g[0] = 0.1
                r[1] += 0.1
            g[1] = 0.1
            g[0] = 0.1
            r[1] = 0.1
            r[0] += 0.1
        g[1] = 0.1
        g[0] = 0.1
        r[1] = 0.1
        r[0] = 0.1
        lamb[1] += 0.1
    asfile.close()


def Test():

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(thread_function, range(9))


def combine_csv():
    os.chdir("cars_pack_py//results//")

    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv("test.csv",
                        index=False, encoding='utf-8')

#time_service = [[60, 0.5], [3], [60, 0.5], [0, 0.5], [3]]


def get_grid(lamb: list, time: list, r: list, g: list, time_service: list, count_serviced_cars: int, K: int):

    f = True
    count_cars = 5000
    sd = ServiceDevice()

    t1 = time_service[0][1]
    t3 = time_service[2][1]

    sd = ServiceDevice()

    tabl = np.zeros((int(K - t3 - time_service[1][0] - time_service[4]
                    [0]), int(K - t1 - time_service[1][0] - time_service[4][0])))

    print(tabl.shape)

    result = np.zeros(len(lamb))

    index_i = tabl.shape[0] - 1
    index_j = 0

    while t1 + time_service[1][0] + t3 + time_service[3][0] <= K and sd.check_gamma(result):
        while t1 + time_service[1][0] + t3 + time_service[3][0] <= K and sd.check_gamma(result):
            prev = sd.Start(lamb, time, r, g, time_service, count_cars)
            b = count_cars
            while f:
                b += count_cars
                result = sd.Start(lamb, time, r, g, time_service, b)
                if result[0] == -1 or result[2] == -1:
                    tabl[index_i, index_j] = -1
                    break
                if abs(result[0] - prev[0]) <= EPSILON_TIME and abs(result[1] - prev[1]) <= EPSILON_DISPERSION and abs(result[2] - prev[2]) <= EPSILON_TIME and abs(result[3] - prev[3]) <= EPSILON_DISPERSION:
                    avg = sd.get_weight_avg_gamma(lamb, [result[0], result[2]])
                    tabl[index_i, index_j] = avg
                    f = False
            result = np.zeros((len(lamb)))
            t1 += 1
            index_i -= 1
        t1 = time_service[0][1]
        index_i = tabl.shape[0] - 1
        index_j += 1
        t3 += 1

    print(tabl)
