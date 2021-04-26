#pragma once

#include "Model.h"

class ModelBartlet : public Model {

  protected:
    const double r;
    const double g;

  public:
    ModelBartlet();
    ModelBartlet(double r, double g);

    double getExpectedValue() const;
    double getExpectedValue(double r_, double g_) const;
    size_t countRequests() override;

    double getProbably(size_t k);
};
