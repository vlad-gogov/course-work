#include <iostream>
#include <cmath>
#include "Model.h"

int main()
{
	Model temp(0.01, 50);
	temp.createModel();
	temp.print();

	return 0;
}