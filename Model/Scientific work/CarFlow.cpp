#include "CarFlow.h"
#include "ModelPoisson.h"
#include "ModelBartlet.h"

#include <iostream>

constexpr double DISTANCE_PACK = 5.0;

CarFlow::CarFlow() : lambda(0), r(0), g(0), time(0) {}

CarFlow::CarFlow(double lamda_, double time_, double r_, double g_) : lambda(lamda_), time(time_),  r(r_), g(g_) {}

bool CarFlow::checkDistPack(const std::vector<double>& slow_cars) const {
	size_t count_slow_cars = slow_cars.size();
	for (size_t i = 0; i < count_slow_cars - 1; i++) {
		if (slow_cars[i + 1] - slow_cars[i] < DISTANCE_PACK)
			return false;
	}
	return true;
}

std::vector<double> CarFlow::createCarsSlow() {
	size_t all_count_requests = 0;
	double full_time = 0;
	ModelPoisson model(lambda, time);
	std::cout << "Poisson:" << std::endl;
	do {
		all_count_requests += model.countRequests();
		full_time += time;
		std::cout << ". Count requests = " << all_count_requests << ". Time = " << full_time << ". "
			<< "|" << all_count_requests / full_time << " - " << lambda << "| < " << 0.1 * lambda << std::endl;
	} while (std::abs(all_count_requests / full_time - lambda) < 0.1 * lambda);
	time = full_time;

	std::vector<double> slow_cars;
	do {
		slow_cars.clear();
		for (size_t i = 0; i < all_count_requests; i++) {
			slow_cars.push_back(generateProbability() * time);
		}
		std::sort(slow_cars.begin(), slow_cars.end());
	} while (!checkDistPack(slow_cars));

	return slow_cars;
}

std::vector<double> CarFlow::buildPack(double average_pack_length, double time_start, size_t count_fast_cars) {
	std::vector<double> pack;
	for (size_t i = 0; i < count_fast_cars; i++) {
		double time_moment;
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
	size_t count_pack = slow_cars.size();
	std::vector<CarsPack> flow_cars(count_pack);

	for (size_t i = 0; i < count_pack; i++) {
		flow_cars[i].first = 1ull;
		flow_cars[i].second.push_back(slow_cars[i]);
		std::cout << flow_cars[i].second[0] << ", ";
	}
	std::cout << std::endl;


	// Fast cars
	ModelBartlet model(r, g);
	std::vector<std::vector<double>> pack_cars_fast;
	double full_time = time;
	double r_stat = 0;
	double expected_value_stat = 0;
	double lambda_bartlet_stat = 0;
	double average_pack_length = 0;
	double expected_value = model.getExpectedValue();
	double lambda_bartlet = lambda * expected_value;

	std::vector<size_t> count_fast_car;

	std::cout << std::endl << "Bartlet" << std::endl;

	do {
		count_fast_car.clear();
		double delta_min_time = std::numeric_limits<double>::max();
		size_t max_count_fast_cars = std::numeric_limits<size_t>::min();
		size_t pack_fast = 0;

		for (size_t i = 0; i < count_pack; i++) {
			size_t count_fast_cars = model.countRequests();
			count_fast_car.push_back(count_fast_cars);
			flow_cars[i].first += count_fast_cars;

			size_t temp = count_fast_car[i];
			if (temp > 1)
				pack_fast++;
			if (max_count_fast_cars < temp)
				max_count_fast_cars = temp;
		}

		for (size_t i = 1; i < count_pack; i++) {
			double delta = slow_cars[i] - slow_cars[i - 1];
			if (delta < delta_min_time)
				delta_min_time = delta;
		}

		average_pack_length = delta_min_time / max_count_fast_cars;

		std::cout << std::endl << delta_min_time << " / " << max_count_fast_cars << " = " << average_pack_length << std::endl;

		r_stat = static_cast<double>(pack_fast) / count_pack;
		expected_value_stat = model.getExpectedValue(r_stat, average_pack_length);
		lambda_bartlet_stat = lambda * expected_value_stat;

	} while (std::abs(r_stat - r) < 0.1 * r &&
		std::abs(expected_value_stat - expected_value) < 0.1 * expected_value &&
		std::abs(lambda_bartlet_stat - lambda_bartlet) < 0.1 * lambda_bartlet);


	for (size_t i = 0; i < count_pack; i++) {
		std::vector<double> pack = buildPack(average_pack_length, slow_cars[i], count_fast_car[i]);
		flow_cars[i].second.insert(flow_cars[i].second.end(), pack.begin(), pack.end());
	}

	return flow_cars;
}
