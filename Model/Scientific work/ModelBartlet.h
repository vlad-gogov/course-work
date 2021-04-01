#pragma once
#include <cmath>
#include <random>

class ModelBartlet {

private:
	double eps;
	double generateProbability();

protected:
	double lambda;
	double r;
	double j;
	size_t count_requests;

public:
	ModelBartlet();
	ModelBartlet(double r, double j, double lambda_stat);
	void countRequests();

	double getProbably(size_t k);
};