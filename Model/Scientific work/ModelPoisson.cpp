#include "ModelPoisson.h"

#include <cmath>
#include <iostream>

ModelPoisson::ModelPoisson() : time(0) {
}

ModelPoisson::ModelPoisson(double lambda_, double time_) : Model(lambda_), time(time_) {
}

int ModelPoisson::countRequests() {
    int count = 0;
    double p = generateProbability();
    std::cout << "Random = " << p;
    p *= exp(lambda * time);
    if (abs(1 - p) <= eps)
        return 0;
    double l = 1;
    double F = l;
    while (F <= p) {
        count++;
        l *= lambda * time / count;
        if (l <= eps)
            return count;
        F += l;
    }
    return count;
}

bool ModelPoisson::isCorrect(int count_requests_, double time_) const {
    return std::abs(count_requests_ / time_ - lambda) < 0.1 * lambda;
}

void ModelPoisson::createModel() {
    double full_time = time;
    int count = 0;
    while (true) {
        count += countRequests();
        std::cout << ". Count requests = " << count << ". Time = " << time << ". "
                  << "|" << count / time << " - " << lambda << "| < " << 0.1 * lambda << std::endl;
        if (isCorrect(count, full_time))
            break;
        full_time += time;
    }
    time = full_time;
    requests.resize(count);
    for (size_t i = 0; i < count; i++) {
        requests[i] = generateProbability() * time;
    }

    std::sort(requests.begin(), requests.end());
}

void ModelPoisson::print() const {
    size_t size = requests.size();
    std::cout << "Lambda = " << lambda << ". Time = " << time << ". Count requests = " << size << "." << std::endl;
    for (size_t i = 0; i < size; i++) {
        std::cout << requests[i];
        if (i < size - 1)
            std::cout << ", ";
    }
    std::cout << ";" << std::endl;
}
