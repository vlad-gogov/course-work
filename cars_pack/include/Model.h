#pragma once

#include <random>

#include "RandomGenerator.h"

class Model : public RandomGenerator {

  protected:
    Model() = default;

    virtual size_t countRequests() = 0;

    virtual ~Model() = default;
};
