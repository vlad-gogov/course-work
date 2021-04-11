#include "CarFlow.h"
#include "ModelPoisson.h"
#include "ModelBartlet.h"

#include <iostream>

const double CarFlow::eps = 1e-3;

CarFlow::CarFlow() : lambda(0), r(0), g(0), time(0) {}

CarFlow::CarFlow(double lamda_, double time_, double r_, double g_) : lambda(lamda_), time(time_),  r(r_), g(g_), 
																		mersenne(rd()), urd(0.0, 1.0 - eps) {}

double CarFlow::generateProbability() const {
	return urd(mersenne);
}

std::vector<double> CarFlow::createCarsSlow() {
	size_t all_count_requests = 0;
	double full_time = 0;
	ModelPoisson model(lambda, time);
	do {
		all_count_requests += model.countRequests();
		full_time += time;
		std::cout << ". Count requests = " << all_count_requests << ". Time = " << time << ". "
			<< "|" << all_count_requests / full_time << " - " << lambda << "| < " << 0.1 * lambda << std::endl;
	} while (std::abs(all_count_requests / full_time - lambda) < 0.1 * lambda);
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


	// Fast cars
	ModelBartlet model(lambda, time, r, g); // TODO
	std::vector<std::vector<double>> pack_cars_fast;
	double full_time = time;
	double r_stat = 0;
	double expected_value_stat = 0;
	double lambda_bartlet_stat = 0;
	double average_pack_length = 0;
	double expected_value = model.getExpectedValue();
	double lambda_bartlet = lambda * expected_value;

	std::vector<size_t> count_fast_car;

	do {
		count_fast_car.clear();
		double delta_min_time = std::numeric_limits<double>::max();
		size_t pack_fast = 0;

		for (size_t i = 0; i < count_pack; i++) {
			count_fast_car.push_back(model.countRequests());
			if (count_fast_car[i] > 1)
				pack_fast++;
		}

		for (size_t i = 1; i < count_pack; i++) {
			double delta = slow_cars[i] - slow_cars[i - 1];
			if (delta < delta_min_time)
				delta_min_time = delta;
		}

		double max_count_fast_cars = *std::max_element(slow_cars.begin(), slow_cars.end());

		average_pack_length = delta_min_time / max_count_fast_cars;

		r_stat = pack_fast / count_pack;
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
