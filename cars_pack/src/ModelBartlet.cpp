#include "ModelBartlet.h"

#include <algorithm>
#include <iostream>
#include <cmath>

#include "ModelPoisson.h"

ModelBartlet::ModelBartlet() : r(0), g(0) {
}

ModelBartlet::ModelBartlet(double r_, double g_) : r(r_), g(g_) {
}

size_t ModelBartlet::countRequests() {
    double p = generateProbability();
    std::cout << "Random: " << p;
    int count = 0;
    double F = 1.0 - r;
    std::cout << " F: " << F;
    double l = 0.0;
    double temp_g = 1;
    double temp = r * (1.0 - g);
    while (F <= p) {
        count++;
        l = temp * temp_g;
        F += l;
        if (std::abs(l) <= eps)
            return count + 1ull;
        temp_g *= g;
    }
    std::cout << " Count: " << count << std::endl;
    return count;
}

double ModelBartlet::getExpectedValue() const {
    return 1 + (r / 1 - g);
}

double ModelBartlet::getExpectedValue(double r_, double g_) const {
    return 1 + (r_ / 1 - g_);
}

double ModelBartlet::getProbably(size_t k) {
    if (k == 1)
        return 1 - r;
    else if (k >= 2)
        return r * (1 - g) * pow(g, k - 2);
    return 0;
}
