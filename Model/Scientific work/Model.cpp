#include "Model.h"

const double Model::eps = 1e-3;

Model::Model() : lambda(0), mersenne(rd()), urd(0.0, 1.0 - eps) {
}

Model::Model(double lambda_) : lambda(lambda_) {
}

double Model::generateProbability() const {
    return urd(mersenne);
}
