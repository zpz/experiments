#include "Python.h"
#include "pybind11/pybind11.h"

#include <iostream>
#include <string>
#include <vector>

namespace py = pybind11;


void test()
{
    py::list x(3);
    x[0] = 1;
    x[1] = "abc";
    x[2] = py::none();
    py::print(x);
    py::print(py::str(x));
    std::cout << py::str(x).cast<std::string>() << std::endl;
}


int main()
{
    Py_Initialize();
    test();
    return 0;
}
