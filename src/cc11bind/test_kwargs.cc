#include "Python.h"
#include "pybind11/pybind11.h"

#include "util.h"

#include <iostream>
#include <map>
#include <string>
#include <vector>

namespace py = pybind11;


void test_dictref()
{
    std::vector<int> intvec{1, 3, 5};

    auto module = py::module::import("py4cc.stl");
    auto cumsum = module.attr("cumsum");

    print("passing vec into dict by ref");
    auto kwargs = py::dict(py::arg("x") = py::cast(&intvec, py::return_value_policy::reference));

    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(**kwargs);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);
}


void test_ref()
{
    // Calling by ref has trouble with passing by keywords.
    // The following will not work:
    //
    //  auto kwargs = py::dict(py::arg("x") = &x);
    //  f(**kwargs);
    //
    //  f(py::arg("x") = &x);
    //
    // However, this works:
    //
    //  auto args = py::list();
    //  args.append(&x);
    //  f(*args);
    // This will pass `x` by reference.

    std::vector<int> intvec{1, 3, 5};

    auto module = py::module::import("py4cc.stl");
    auto cumsum = module.attr("cumsum");

    auto kwargs = py::dict(py::arg("x") = intvec);
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(**kwargs);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);

    std::cout << std::endl;
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(py::arg("x") = intvec);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);

    std::cout << std::endl;
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(**py::dict(py::arg("x") = intvec));
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);

    auto args = py::list();
    args.append(intvec);
    std::cout << std::endl;
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(*args);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);

    auto args2 = py::list();
    args2.append(&intvec);
    std::cout << std::endl;
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(*args2);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);
}


int main()
{
    Py_Initialize();
    py::module::import("py4cc._cc11binds");

    test_ref();
    print();
    test_dictref();
    return 0;
}
