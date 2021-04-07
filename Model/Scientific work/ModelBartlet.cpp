#include "ModelBartlet.h"

#include <cmath>

#include "ModelPoisson.h"

ModelBartlet::ModelBartlet() : r(0), g(0) {
}

ModelBartlet::ModelBartlet(double lambda_, double r_, double g_) : Model(lambda_), r(r_), g(g_) {
}

int ModelBartlet::countRequests() {
    double p = generateProbability();
    int count = 0;
    double F = 1.0 - r;
    double l = 1.0;
    double temp_g = 1;
    while (F <= p) {
        count++;
        l += r * (1.0 - g) * temp_g;
        F += l;
        if (std::abs(l) <= eps)
            return count + 1;
        temp_g *= g;
    }
    return count;
}

bool ModelBartlet::isCorrect(double lambda_stat, double r_stat, double expected_value_stat,
                             double lambda_bertlet_stat) const {
    double lambda_bartlet = getLambdaBartlet();
    double expected_value = 1 + r / (1 - g);
    return (std::abs(lambda_stat - lambda) < 0.1 * lambda && std::abs(r_stat - r) < 0.1 * r &&
            std::abs(expected_value_stat - expected_value) < 0.1 * expected_value &&
            std::abs(lambda_bertlet_stat - lambda_bartlet) < 0.1 * lambda_bartlet);
}

void ModelBartlet::createModel() {
	// TODO: Implementation
}

double ModelBartlet::getLambdaBartlet() const {
    return lambda * (1 + (r / 1 - g));
}

double ModelBartlet::getProbably(size_t k) {
    if (k == 1)
        return 1 - r;
    else if (k >= 2)
        return r * (1 - g) * pow(g, k - 2);
    return 0;
}
