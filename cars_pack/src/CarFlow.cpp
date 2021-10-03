#include "CarFlow.h"
#include "ModelBartlet.h"
#include "ModelPoisson.h"

#include <iostream>

constexpr double DISTANCE_PACK = 3.0;

CarFlow::CarFlow() : lambda(0), time(0), r(0), g(0) {
}

CarFlow::CarFlow(double lamda_, double time_, double r_, double g_) : lambda(lamda_), time(time_), r(r_), g(g_) {
}

std::vector<CarsPack> CarFlow::checkDistPack(const std::vector<double>& slow_cars) const {
    size_t count_slow_cars = slow_cars.size();
    std::vector<CarsPack> result;
    result.push_back(CarsPack(1, {slow_cars[0]}));
    size_t index_pack = 0;
    double temp = slow_cars[0];
    for (size_t i = 1; i < count_slow_cars; i++) {
        if (slow_cars[i] - temp <= DISTANCE_PACK) {
            result[index_pack].first++;
            result[index_pack].second.push_back(slow_cars[i]);
        } else {
            result.push_back(CarsPack(1ull, {slow_cars[i]}));
            index_pack++;
            temp = slow_cars[i];
        }
    }
    return result;
}

std::vector<double> CarFlow::createCarsSlow() {
    size_t all_count_requests = 0;
    double full_time = 0;
    double lambda_b = lambda / (1 + r / (1 - g));
    ModelPoisson model(lambda_b, time);
    std::cout << "Poisson:" << std::endl;
    do {
        all_count_requests += model.countRequests();
        full_time += time;
        std::cout << ". Count requests = " << all_count_requests << ". Time = " << full_time << ". "
                  << "|" << all_count_requests / full_time << " - " << lambda_b << "| < " << 0.1 * lambda_b
                  << std::endl;
    } while (std::abs(all_count_requests / full_time - lambda_b) >= 0.1 * lambda_b);
    time = full_time;

    std::vector<double> slow_cars;
    for (size_t i = 0; i < all_count_requests; i++) {
        slow_cars.push_back(generateProbability() * time);
    }
    std::sort(slow_cars.begin(), slow_cars.end());

    return slow_cars;
}

std::vector<double> CarFlow::buildPack(double average_pack_length, double time_start, size_t count_fast_cars) {
    std::vector<double> pack;
    for (size_t i = 0; i < count_fast_cars; i++) {
        double time_moment = 0;
        do {
            double p = generateProbability();
            time_moment = time_start + p * average_pack_length;
        } while (time_moment > time);
        pack.push_back(time_moment);
    }
    std::sort(pack.begin(), pack.end());
    return pack;
}

std::vector<CarsPack> CarFlow::createFlow() {

    // Slow cars
    std::vector<double> slow_cars = createCarsSlow();
    std::vector<CarsPack> flow_cars = checkDistPack(slow_cars);
    size_t count_pack = flow_cars.size();

    if (r != 0 && g != 0) {

        // Fast cars
        constexpr int c = 2;
        ModelBartlet model_bartlet(r, g);
        double r_stat = 0;
        double expected_value_stat = 0;
        double lambda_bartlet_stat = 0;
        double average_pack_length = 0;
        double expected_value = model_bartlet.getExpectedValue();

        double lambda_bartlet = lambda * expected_value;

        std::vector<size_t> count_fast_car;

        std::cout << std::endl << "Bartlet:" << std::endl;

        do {
            count_fast_car.clear();
            double delta_min_time = std::numeric_limits<double>::max();
            size_t max_count_fast_cars = std::numeric_limits<size_t>::min();
            size_t pack_fast = 0;

            for (size_t i = 0; i < count_pack; i++) {
                count_fast_car.push_back(model_bartlet.countRequests());
                size_t temp = count_fast_car[i];
                if (temp > 0)
                    pack_fast++;
                if (max_count_fast_cars < temp)
                    max_count_fast_cars = temp;
            }

            for (size_t i = 1; i < count_pack; i++) {
                double delta = slow_cars[i] - slow_cars[i - 1];
                if (delta < delta_min_time)
                    delta_min_time = delta;
            }

            average_pack_length = delta_min_time / (max_count_fast_cars + c);

            std::cout << std::endl
                      << delta_min_time << " / " << max_count_fast_cars + c << " = " << average_pack_length
                      << std::endl;

            r_stat = static_cast<double>(pack_fast) / count_pack;
            expected_value_stat = model_bartlet.getExpectedValue(r_stat, average_pack_length);
            lambda_bartlet_stat = lambda * expected_value_stat;

        } while (std::abs(r_stat - r) < 0.1 * r &&
                 std::abs(expected_value_stat - expected_value) < 0.1 * expected_value &&
                 std::abs(lambda_bartlet_stat - lambda_bartlet) < 0.1 * lambda_bartlet);

        for (size_t i = 0; i < count_pack; i++) {
            if (count_fast_car[i] + 1 == flow_cars[i].first)
                continue;
            if (count_fast_car[i] + 1 > flow_cars[i].first) {
                std::vector<double> pack =
                    buildPack(average_pack_length, flow_cars[i].second[0], count_fast_car[i] - flow_cars[i].first);
                flow_cars[i].second.insert(flow_cars[i].second.end(), pack.begin(), pack.end());
            } else if (count_fast_car[i] < flow_cars[i].first) {
                while (count_fast_car[i] + 1 < flow_cars[i].first) {
                    flow_cars[i].first--;
                    flow_cars[i].second.pop_back();
                }
            }
        }
    }

    return flow_cars;
}

double CarFlow::getTime() const {
    return time;
}
