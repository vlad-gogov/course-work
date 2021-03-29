#include <iostream>
#include <cmath>
#include "Model.h"

int main()
{
	Model a(0.01, 50);
	a.createModel();
	a.print();
	std::cout << std::endl;

	Model b(0.1, 50);
	b.createModel();
	b.print();
	std::cout << std::endl;

	Model c(0.5, 50);
	c.createModel();
	c.print();
	std::cout << std::endl;

	Model d(0.1, 10);
	d.createModel();
	d.print();
	std::cout << std::endl;

	return 0;
}