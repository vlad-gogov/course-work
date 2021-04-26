#pragma once

#include <random>

class RandomGenerator
{
	mutable std::random_device rd;
	mutable std::mt19937 mersenne;
	mutable std::uniform_real_distribution<double> urd;

protected:
	static const double eps;

public:
	RandomGenerator();
	~RandomGenerator() = default;

	double generateProbability() const;
};
