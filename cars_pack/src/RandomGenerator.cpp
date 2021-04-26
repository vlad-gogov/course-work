#include "RandomGenerator.h"

const double RandomGenerator::eps = 1e-3;


RandomGenerator::RandomGenerator() : mersenne(rd()), urd(0.0, 1.0 - eps) {
}


double RandomGenerator::generateProbability() const {
    return urd(mersenne);
}
