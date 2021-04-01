#pragma once
#include <vector>
#include <ostream>
#include <iostream>
#include <random>

class ModelPoisson {
protected:
	double lambda;
	double time;
	size_t count_requests;
	size_t prev_count_requests;
	std::vector<double> requests;
	double lambda_stat;

private:
	double eps;
	double generateProbability();
	void countRequests(double part_time);
	bool isCorrect();

public:
	ModelPoisson();
	ModelPoisson(double lambda_, double time_);
	~ModelPoisson() = default;

	void createModelPoisson();
	void print();
	double getLambdaStat();
};