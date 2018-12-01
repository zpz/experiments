#include <cc_version03.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>


namespace py = pybind11;


py::array_t<long> weekdays_py(py::array_t<long> ts)
{
    long n = ts.size();
    py::array_t<long> out = py::array_t<long>(n);
    _weekdays(ts.data(), out.mutable_data(), n);
    return out;
}


PYBIND11_MODULE(cc_version03, m)
{
    m.def("weekday", &weekday);
    m.def("weekdays", &weekdays_py);
}