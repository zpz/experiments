#include "Python.h"
#include "pybind11/pybind11.h"
//#include "pybind11/stl.h"
    // incuding this will enforce passing by value, even if using `&x` to pass

// Do not `#include stl.h`,
// and do `import _cc11binds`,
// then `&x` will pass by ref, but `x` wil still pass by value.
// STL containers become custom type on Python side.

// Do `#include stl.h`,
// then `&x` and `x` will both pass by value,
// even with `import _cc11binds`.
// STL containers become native Python `list`, `dict`, etc on Python side.

// With
// `const std::vector<..> & x`
// Passing `&x` into Python will ignore `const`.

#include "util.h"

#include <iostream>
#include <map>
#include <string>
#include <vector>

namespace py = pybind11;


void test_const(const std::vector<int> & intvec, py::object cumsum)
{
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(&intvec);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);
}


void test_noconst(std::vector<int> & intvec, py::object cumsum)
{
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(&intvec);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);
}


void test_ref()
{
    std::vector<int> intvec{1, 3, 5};
    std::vector<std::string> strvec{"abc", "def", "this is good"};
    std::map<std::string, double> doublemap{{"first", 1.1}, {"second", 2.2}, {"third", 3.3}};

    auto module = py::module::import("py4cc.stl");
    auto cumsum = module.attr("cumsum");
    auto mapadd = module.attr("mapadd");

    // Pass pointers.

    std::cout << "=== pass as `&x` ===" << std::endl;
    
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(intvec);
    cumsum(&intvec);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(intvec);

    std::cout << std::endl;
    std::cout << "before `cumsum`, in C++ --- ";
    print_vec<>(strvec);
    cumsum(&strvec);
    std::cout << "after `cumsum`, in C++ --- ";
    print_vec<>(strvec);

    std::cout << std::endl;
    std::cout << "before `mapadd`, in C++ --- ";
    print_map<>(doublemap);
    mapadd(&doublemap);
    std::cout << "after `mapadd`, in C++: ";
    print_map<>(doublemap);


    // Pass values.
    std::cout << std::endl << "=== pass as `x`===" << std::endl;

    std::cout << std::endl;
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

    // Test constness violation
    std::cout << std::endl << "=== test const ===" << std::endl << std::endl;
    test_const(intvec, cumsum);

    std::cout << std::endl << "=== test noconst ===" << std::endl << std::endl;
    test_noconst(intvec, cumsum);
}


int main()
{
    Py_Initialize();
    py::module::import("py4cc._cc11binds");
    test_ref();
    return 0;
}
