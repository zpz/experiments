#include "datex/cc_version01.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>


namespace py = pybind11;


PYBIND11_MODULE(version01, m)
{
    m.def("weekday", &weekday);
    m.def("weekdays", &weekdays);
    m.def("vectorized_weekday", py::vectorize(weekday));
}