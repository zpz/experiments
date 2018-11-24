#include "Python.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

#include "util.h"

#include <iostream>
#include <map>
#include <vector>
#include <string>

namespace py = pybind11;


void test_copy()
{
    std::vector<int> intvec{1, 3, 5};
    std::vector<std::string> strvec{"abc", "def", "this is good"};
    std::map<std::string, double> doublemap{{"first", 1.1}, {"second", 2.2}, {"third", 3.3}};

    auto module = py::module::import("py4cc.stl");
    auto cumsum = module.attr("cumsum");
    auto mapadd = module.attr("mapadd");

    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(intvec);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);

    std::cout << std::endl;
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(strvec);
    cumsum(strvec);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(strvec);

    std::cout << std::endl;
    std::cout << "before `mapadd`, in C++ --- ";
    print_map<>(doublemap);
    mapadd(doublemap);
    std::cout << "after `mapadd`, in C++: ";
    print_map<>(doublemap);
    std::cout << std::endl;
}


int main()
{
    Py_Initialize();
    test_copy();
    return 0;
}
