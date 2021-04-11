#include "CarFlow.h"

#include <iostream>

int main() {
    CarFlow a(0.1, 50, 0.5, 0.5);
    std::vector<CarsPack> b = a.createFlow();

    return 0;
}
