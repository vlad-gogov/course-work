#include "CarFlow.h"

#include <iostream>

void print(const std::vector<CarsPack>& temp) {
    size_t count_pack = temp.size();
    std::cout << std::endl;
    for (size_t i = 0; i < count_pack; i++) {
        size_t size_pack = temp[i].first;
        std::cout << "#" << i + 1 << " pack: ";
        for (size_t j = 0; j < size_pack; j++) {
            std::cout << temp[i].second[j];
            if (j != size_pack - 1)
                std::cout << ", ";
        }
        std::cout << std::endl;
    }
}

int main() {
    CarFlow a(0.1, 120, 0.9, 0.6);
    std::vector<CarsPack> b = a.createFlow();
    print(b);

    return 0;
}
