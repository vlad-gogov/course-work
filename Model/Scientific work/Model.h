#pragma once
#include <vector>
#include <ostream>
#include <iostream>

class Model {
protected:
	double lambda;
	double time;
	size_t count_requests;
	size_t prev_count_requests;
	std::vector<double> requests;

private:
	double eps;
	double generateProbability();
	void countRequests(double part_time);
	bool isCorrect();

public:
	Model();
	Model(double lambda_, double time_);
	~Model() = default;

	void createModel();
	void print();
};