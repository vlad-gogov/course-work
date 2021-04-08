#include "ModelBartlet.h"

#include <cmath>
#include <algorithm>

#include "ModelPoisson.h"

ModelBartlet::ModelBartlet() : time(0), r(0), g(0) {
}

ModelBartlet::ModelBartlet(double lambda_, double time_, double r_, double g_) : Model(lambda_), time(time_), r(r_), g(g_) {
}

int ModelBartlet::countRequests() {
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
            return count + 1;
        temp_g *= g;
    }
    return count;
}

bool ModelBartlet::isCorrect(double r_stat, double expected_value_stat,
                             double lambda_bertlet_stat) const {
    double lambda_bartlet = lambda * getExpectedValue();
    double expected_value = 1 + r / (1 - g);
    return (std::abs(r_stat - r) < 0.1 * r &&
            std::abs(expected_value_stat - expected_value) < 0.1 * expected_value &&
            std::abs(lambda_bertlet_stat - lambda_bartlet) < 0.1 * lambda_bartlet);
}

void ModelBartlet::createModel() {
	double full_time = time;
    double r_stat = 0, expected_value_stat = 0, lambda_bertlet_stat = 0;
    do {
        ModelPoisson slow_cars(lambda, time);
        slow_cars.createModel();
        size_t count_slow_cars = slow_cars.getRequests().size();
        std::vector<size_t> count_fast_car;
        double delta_min_time = std::numeric_limits<double>::max();

        for (size_t i = 0; i < count_slow_cars; i++) {
            count_fast_car.push_back(countRequests());
        }

        for (size_t i = 1; i < count_slow_cars; i++) {
            double delta = slow_cars.getRequests()[i] - slow_cars.getRequests()[i - 1];
            if (delta < delta_min_time)
                delta_min_time = delta;
        }

        double max_count_fast_cars = *std::max_element(slow_cars.getRequests().begin(), slow_cars.getRequests().end());

        double average_pack_length = delta_min_time / max_count_fast_cars;

        for (size_t i = 0; i < count_slow_cars; i++) {
            buildPack(average_pack_length, slow_cars.getRequests()[i], count_fast_car[i]);
        }

        size_t count_pack = requests.size();

        for (size_t i = 0; i < count_pack; i++) {
        }

    } while (isCorrect(r_stat, expected_value_stat, lambda_bertlet_stat)); // TODO
}

void ModelBartlet::buildPack(double average_pack_length, double time_start, size_t count_fast_cars) {
    std::vector<double> pack;
    for (size_t i = 0; i < count_fast_cars; i++) {
        double time_moment;
        do {
            double p = generateProbability();
            time_moment = p * average_pack_length;
        } while (time_moment > time);
        pack.push_back(time_moment);
    }

    std::sort(pack.begin(), pack.end());

    requests.insert({count_fast_cars, pack});
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
