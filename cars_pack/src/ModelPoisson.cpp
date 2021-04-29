#include "ModelPoisson.h"

#include <cmath>
#include <iostream>

ModelPoisson::ModelPoisson() : lambda(0), time(0){
}

ModelPoisson::ModelPoisson(double lambda_, double time_) : lambda(lambda_), time(time_) {
}

size_t ModelPoisson::countRequests() {
    size_t count = 0;
    double p = generateProbability();
    double a = lambda * time;
    std::cout << "Random = " << p;
    p *= exp(a);
    if (abs(1 - p) <= eps)
        return 0;
    double l = 1;
    double F = l;
    while (F <= p) {
        count++;
        l *= a / count;
        if (l <= eps)
            return count;
        F += l;
    }
    return count;
}

bool ModelPoisson::isCorrect(int count_requests_, double time_) const {
    return std::abs(count_requests_ / time_ - lambda) < 0.1 * lambda;
}
