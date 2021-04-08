#pragma once

#include "Model.h"

#include <unordered_map>

class ModelBartlet : public Model {
    int countRequests() override;
    bool isCorrect(double r_stat, double expected_value_stat, double lambda_bertlet_stat) const;
    void buildPack(double average_pack_length, double time_start, size_t count_fast_cars);

  protected:
    double time;
    const double r;
    const double g;
    std::unordered_map<size_t, std::vector<double>> requests;

  public:
    ModelBartlet();
    ModelBartlet(double lambda_, double time_, double r, double j);

    double getExpectedValue() const;
    double getExpectedValue(double r_, double g_) const;

    void createModel() override;

    double getProbably(size_t k);
};
