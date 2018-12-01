#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>


long weekday(long ts) 
{
    long ts0, weekday0, DAY_SECONDS, WEEK_SECONDS;
    long ts_delta, td, nday, weekday;

    ts0 = 1489363200;   // 2017-03-13 0:0:0 UTC, Monday
    weekday0 = 1;       // ISO weekday: Monday is 1, Sunday is 7

    DAY_SECONDS = 86400;
    WEEK_SECONDS = 604800;

    ts_delta = ts - ts0;
    if (ts_delta < 0) {
        ts_delta += ((-ts_delta) / WEEK_SECONDS + 1) * WEEK_SECONDS;
    }

    td = ts_delta % WEEK_SECONDS;
    nday = td / DAY_SECONDS;
    weekday = weekday0 + nday;
    if (weekday > 7) {
        weekday = weekday - 7;
    }
    return weekday;
}


namespace py = pybind11;


py::array_t<long> weekdays(py::array_t<long> ts)
{
    long n = ts.size();
    py::array_t<long> out = py::array_t<long>(n);
    auto input = ts.data();
    auto output = out.mutable_data();
    for (long i = 0; i < n; i++) {
        output[i] = weekday(input[i]);
    }
    return out;
}


PYBIND11_MODULE(cc_version02, m)
{
    m.def("weekdays", &weekdays);
    m.def("vectorized_weekday", py::vectorize(weekday));
}