#include <cc_version04.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>


namespace py = pybind11;


py::array_t<long> weekdays_py(py::array_t<long> ts)
{
    long n = ts.size();
    py::array_t<long> out = py::array_t<long>(n);
    _weekdays(n, ts.data(), out.mutable_data());
    return out;
}


PYBIND11_MODULE(cc_version04, m)
{
    m.def("weekdays", &weekdays_py);
}