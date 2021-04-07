#pragma once

#include "Model.h"

#include <unordered_map>

class ModelBartlet : public Model {
    int countRequests() override;
    bool isCorrect(double lambda_stat, double r_stat, double expected_value_stat, double lambda_bertlet_stat) const;

  protected:
    const double r;
    const double g;
    std::unordered_map<size_t, std::vector<double>> requests;

  public:
    ModelBartlet();
    ModelBartlet(double lambda_, double r, double j);

    double getLambdaBartlet() const;

    void createModel() override;

    double getProbably(size_t k);
};
