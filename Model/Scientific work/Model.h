#pragma once

#include <random>

class Model {
    mutable std::random_device rd;
    mutable std::mt19937 mersenne;
    mutable std::uniform_real_distribution<double> urd;

  protected:
    static const double eps;
    const double lambda;

    Model();
    Model(double lambda_);

    double generateProbability() const;
    virtual size_t countRequests() = 0;

    virtual ~Model() = default;
};
