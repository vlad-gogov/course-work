#include "ModelBartlet.h"

ModelBartlet::ModelBartlet() {
	lambda = 0;
	r = 0;
	j = 0;
	eps = 1.0e-3;
	count_requests = 0;
}

ModelBartlet::ModelBartlet(double r, double j, double lambda_stat) {
	this->r = r;
	this->j = j;
	lambda = lambda_stat / (1 + r / (1 - j));
	eps = 1.0e-3;
	count_requests = 0;
}

double ModelBartlet::generateProbability() {
	std::random_device rd;
	std::mt19937 mersenne(rd());
	std::uniform_real_distribution<double> urd(0.0, 1.0 - eps);
	double p = urd(mersenne);
	return p;
}

void ModelBartlet::countRequests() {
	double p = generateProbability();
	double F = 1.0 - r;
	double l = 1.0;
	double temp_j = 1;
	while (F <= p) {
		count_requests++;
		l += r * (1 - j) * temp_j;
		temp_j *= j;
	}
}

double ModelBartlet::getProbably(size_t k) {
	if (k == 1)
		return 1 - r;
	else if (k >= 2)
		return r * (1 - j) * pow(j, k - 2);
	return 0;
}

