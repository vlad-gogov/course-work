import csv
from os import write
from ..backend.service_device import ServiceDevice


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


def Test():

    with open("test.csv", "w", encoding='utf-8') as asfile:
        fieldnames = ['№', 'count cars', 'lamb1', 'r1', 'g1',
                      'gamma1', "average length pack 1:", 'lamb2', 'r2', 'g2', 'gamma2', "average length pack 2:"]
        writer = csv.DictWriter(asfile, fieldnames=fieldnames)
        writer.writeheader()

        lamb = [0.1, 0.1]
        time = 100
        r = [0.1, 0.1]
        g = [0.1, 0.1]
        time_service = [[60, 0.5], [3], [60, 0.5], [0, 0.5], [3]]

        f = True
        count_cars = 5000
        sd = ServiceDevice()
        l = 0

        for _ in range(9):

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
                                        writer.writerow({'№': l, 'count cars': b, 'lamb1': lamb[0], 'r1': r[0], 'g1': g[0],
                                                         'gamma1': a[0], "average length pack 1:": avglengt[0], 'lamb2': lamb[1], 'r2': r[1], 'g2': g[1], 'gamma2': a[1], "average length pack 2:": avglengt[1]})
                                        f = False
                                    prev = a
                                f = True
                                l += 1
                                print(l)
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

            g[1] = 0.1
            g[0] = 0.1
            r[1] = 0.1
            r[0] = 0.1
            lamb[1] += 0.1
            lamb[0] += 0.1
