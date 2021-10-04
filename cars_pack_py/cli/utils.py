def averageLengthPack(car_flow: list) -> float:
    dist = 0
    for x in car_flow:
        dist += len(x)
    return dist / len(car_flow)
