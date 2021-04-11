#pragma once

#include "Model.h"

#include <algorithm>
#include <vector>

class ModelPoisson : public Model {
    bool isCorrect(int count_requests_, double time_) const;

  protected:
    double time;

  public:
    ModelPoisson();
    ModelPoisson(double lambda_, double time_);
    ~ModelPoisson() = default;

    size_t countRequests();
};
