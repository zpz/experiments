/*
 Compile:
 g++ -O3 -shared -std=c++11 -fPIC -I /usr/local/include/python3.5m \
      `python-config --cflags --ldflags |sed s/-Wstrict-prototypes//` _cc11binds.cc -o _cc11binds.so
*/

#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

#include <map>
#include <string>
#include <vector>

namespace py = pybind11;

PYBIND11_PLUGIN(_cc11binds) {
    py::module m("_cc11binds", "C++ type bindings created by py11bind");
    py::bind_vector<std::vector<int>>(m, "IntVector");
    py::bind_vector<std::vector<std::string>>(m, "StringVector");
    py::bind_map<std::map<std::string, double>>(m, "StringDoubleMap");
    // 'bind_map` does not create method `values`.

    return m.ptr();
}
