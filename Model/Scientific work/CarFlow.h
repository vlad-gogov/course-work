#pragma once

#include <vector>
#include <utility>
#include <random>

#include "RandomGenerator.h"

using CarsPack = std::pair<size_t, std::vector<double>>;

class CarFlow : public RandomGenerator {

	const double lambda;
	const double r;
	const double g;
	double time;

	bool checkDistPack(const std::vector<double>& slow_cars) const;
	std::vector<double> createCarsSlow();
	std::vector<double> buildPack(double average_pack_length, double time_start, size_t count_fast_cars);

public:
	CarFlow();
	CarFlow(double lamda_, double time_, double r_, double g_);
	std::vector<CarsPack> createFlow();

	~CarFlow() = default;
};
