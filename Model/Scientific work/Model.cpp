#include <random>
#include "Model.h"

Model::Model() {
	lambda = 0;
	time = 0;
	count_requests = 0;
	prev_count_requests = 0;
	eps = 1.0e14;
}

Model::Model(double lambda_, double time_) {
	lambda = lambda_;
	time = time_;
	count_requests = 0;
	prev_count_requests = 0;
	eps = 1.0e14;
}

double Model::generateProbability() {
	std::random_device rd;
	std::mt19937 mersenne(rd());
	std::uniform_real_distribution<double> urd(0.0, 1.0 - std::numeric_limits<double>::epsilon() * eps);
	double p = static_cast<double>(urd(mersenne));
	return p;
}

void Model::countRequests(double part_time) {
	double p = generateProbability();
	std::cout << "Random = " << p;
	p *= exp(lambda * part_time);
	if (abs(1 - p) <= std::numeric_limits<double>::epsilon() * eps)
		return;
	int i = 1;
	double F = 1;
	double l = lambda * part_time;
	while (F <= p) {
		i++;
		l *= lambda * part_time / i;
		if (l <= std::numeric_limits<double>::epsilon() * eps)
			return;
		F += l;
		count_requests++;
	}
}

bool Model::isCorrect() {
	return abs(prev_count_requests / time - lambda) < 0.1 * lambda;
}

void Model::createModel() {
	double current_time = time;
	while (true) {
		countRequests(current_time);
		prev_count_requests += count_requests;
		std::cout << ". Count requests = " << prev_count_requests << ". Time = " << time << ". ";
		std::cout << "|" << prev_count_requests / time << " - " << lambda << "| < " << 0.1 * lambda << std::endl;
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

void Model::print() {
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
