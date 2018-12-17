#include <datex/cc_version01.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>


namespace py = pybind11;


py::array_t<long> weekdays_py(py::array_t<long> ts)
{
    long n = ts.size();
    py::array_t<long> out = py::array_t<long>(n);
    auto p_ts = ts.data();
    auto p_out = out.mutable_data();
    for (long i = 0; i < n; i++) {
        p_out[i] = weekday(p_ts[i]);
    }
    return out;
}


PYBIND11_MODULE(version02, m)
{
    m.def("weekday", &weekday);
    m.def("weekdays", &weekdays_py);
}