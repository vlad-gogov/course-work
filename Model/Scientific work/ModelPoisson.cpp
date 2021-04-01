#include "ModelPoisson.h"

ModelPoisson::ModelPoisson() {
	lambda = 0;
	time = 0;
	count_requests = 0;
	prev_count_requests = 0;
	lambda_stat = 0;
	eps = 1.0e-3;
}

ModelPoisson::ModelPoisson(double lambda_, double time_) {
	lambda = lambda_;
	time = time_;
	count_requests = 0;
	prev_count_requests = 0;
	lambda_stat = 0;
	eps = 1.0e-3;
}

double ModelPoisson::generateProbability() {
	std::random_device rd;
	std::mt19937 mersenne(rd());
	std::uniform_real_distribution<double> urd(0.0, 1.0 - eps);
	double p = urd(mersenne);
	return p;
}

void ModelPoisson::countRequests(double part_time) {
	double p = generateProbability();
	std::cout << "Random = " << p;
	p *= exp(lambda * part_time);
	if (abs(1 - p) <= eps)
		return;
	double l = 1;
	double F = l;
	while (F <= p) {
		count_requests++;
		l *= lambda * part_time / count_requests;
		if (l <= eps)
			return;
		F += l;
	}
}

bool ModelPoisson::isCorrect() {
	lambda_stat = prev_count_requests / time;
	return abs(lambda_stat - lambda) < 0.1 * lambda;
}

void ModelPoisson::createModelPoisson() {
	double current_time = time;
	while (true) {
		countRequests(current_time);
		std::cout << ". Delta requests = " << count_requests << ". ";
		prev_count_requests += count_requests;
		std::cout << "Count requests = " << prev_count_requests << ". Time = " << time << ". ";
		std::cout << "|" << lambda_stat << " - " << lambda << "| < " << 0.1 * lambda << std::endl;
		if (isCorrect())
			break;
		count_requests = 0;
		time += current_time;
	}
	count_requests = prev_count_requests;
	requests.resize(count_requests);
	for (size_t i = 0; i < count_requests; i++) {
		requests[i] = generateProbability() * time;
	}

	std::sort(requests.begin(), requests.end());
}

void ModelPoisson::print() {
	std::cout << "Lambda = " << lambda << ". Time = " << time << ". Count requests = "
		<< count_requests << "." << std::endl;
	size_t size = requests.size();
	for (size_t i = 0; i < size; i++) {
		std::cout << requests[i];
		if (i < size - 1)
			std::cout << ", ";
	}
	std::cout << ";" << std::endl;
}

double ModelPoisson::getLambdaStat() {
	return lambda_stat;
}
