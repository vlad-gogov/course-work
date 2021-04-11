#include "ModelBartlet.h"

#include <cmath>
#include <algorithm>

#include "ModelPoisson.h"

ModelBartlet::ModelBartlet() : time(0), r(0), g(0) {
}

ModelBartlet::ModelBartlet(double lambda_, double time_, double r_, double g_) : Model(lambda_), time(time_), r(r_), g(g_) {
}

size_t ModelBartlet::countRequests() {
    double p = generateProbability();
    int count = 0;
    double F = 1.0 - r;
    double l = 1.0;
    double temp_g = 1;
    while (F <= p) {
        count++;
        l += r * (1.0 - g) * temp_g;
        F += l;
        if (std::abs(l) <= eps)
            return count + 1ull;
        temp_g *= g;
    }
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
