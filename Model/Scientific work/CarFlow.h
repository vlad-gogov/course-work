#pragma once

#include <vector>
#include <utility>
#include <random>

using CarsPack = std::pair<size_t, std::vector<double>>;

class CarFlow {
	mutable std::random_device rd;
	mutable std::mt19937 mersenne;
	mutable std::uniform_real_distribution<double> urd;
	static const double eps;

	const double lambda;
	const double r;
	const double g;
	double time;

	double generateProbability() const;
	std::vector<double> createCarsSlow();
	std::vector<double> buildPack(double average_pack_length, double time_start, size_t count_fast_cars);

public:
	CarFlow();
	CarFlow(double lamda_, double time_, double r_, double g_);
	~CarFlow() = default;
	std::vector<CarsPack> createFlow();
};
