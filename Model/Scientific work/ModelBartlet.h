#pragma once

#include "Model.h"

#include <unordered_map>

class ModelBartlet : public Model {

  protected:
    double time;
    const double r;
    const double g;

  public:
    ModelBartlet();
    ModelBartlet(double lambda_, double time_, double r, double j);

    double getExpectedValue() const;
    double getExpectedValue(double r_, double g_) const;
    size_t countRequests() override;

    double getProbably(size_t k);
};
