#include "ModelPoisson.h"

#include <iostream>

int main() {
    ModelPoisson a(0.01, 50);
    a.createModel();
    a.print();
    std::cout << std::endl;

    ModelPoisson b(0.1, 50);
    b.createModel();
    b.print();
    std::cout << std::endl;

    ModelPoisson c(0.5, 50);
    c.createModel();
    c.print();
    std::cout << std::endl;

    return 0;
}
