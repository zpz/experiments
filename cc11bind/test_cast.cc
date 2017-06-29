#include "Python.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h" 
    // needed for explicit or implicit `cast` of STL containers.
    // "stl_bind.h" won't work.

#include <cassert>
#include <iostream>
#include <map>
#include <string>
#include <tuple>
#include <vector>

namespace py = pybind11;

template<typename T>
void pyprint(const T& x)
{
    py::object y = py::cast(x);
    std::cout 
        << "Python type: " << y.attr("__class__").attr("__name__").cast<std::string>()
        << std::endl
        << "  __repr__: " << y.attr("__repr__")().cast<std::string>()
        << std::endl
        << "  __str__: " << y.attr("__str__")().cast<std::string>()
        << std::endl
        << "  __len__: " << y.attr("__len__")().cast<int>()
        << std::endl << std::endl;
}

void test_cast()
{
    std::vector<int> intvec{1, 3, 5};
    std::vector<std::string> strvec{"abc", "def", "this is good"};
    std::map<std::string, double> doublemap{{"first", 1.1}, {"second", 2.2}, {"third", 3.3}};
    std::tuple<int, double, std::string> misctuple = std::make_tuple(123, 3.1415926, "Captain Cook");

    // explicit cast

    pyprint<>(intvec);
    pyprint<>(strvec);
    pyprint<>(doublemap);
    pyprint<>(misctuple);

    auto z = py::cast(intvec).attr("index")(3);
    auto zz = z.cast<int>();
    std::cout << "3 is at index " << zz << " in " << std::endl;
    assert(zz == 1);

    // implicit cast

    auto show = py::module::import("py4cc.stl").attr("show");

    std::cout << std::endl;
    show(intvec);
    std::cout << std::endl;
    show(strvec);
    std::cout << std::endl;
    show(doublemap);
    std::cout << std::endl;
    show(misctuple);
}


int main()
{
    Py_Initialize();
    test_cast();
    return 0;
}
