#pragma once

#include "Model.h"

#include <vector>

class ModelPoisson : public Model {
    int countRequests();
    bool isCorrect(int count_requests_, double time_) const;

  protected:
    double time;
    std::vector<double> requests;

  public:
    ModelPoisson();
    ModelPoisson(double lambda_, double time_);
    ~ModelPoisson() = default;

    void createModel() override;
    void print() const;
};
