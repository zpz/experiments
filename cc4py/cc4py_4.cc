#include "cc4py_4.h"

#include "Python.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

#include <algorithm>
#include <cassert>
#include <exception>
#include <iostream>
#include <memory>
#include <mutex>


using namespace cc4py;
namespace py = pybind11;

std::mutex py_lock;

Receipt::Receipt()
{
}


Receipt::Receipt(int flag_, std::string const & message_, py::object const & future_)
    : flag(flag_), message(message_), future(future_)
{
    future.inc_ref();
}


Receipt::Receipt(Receipt const & rhs)
    : flag(rhs.flag), message(rhs.message), future(rhs.future)
{
}


Receipt& Receipt::operator=(Receipt const & rhs)
{
    flag = rhs.flag;
    message = rhs.message;
    future = rhs.future;
    return *this;
}


Receipt& Receipt::operator=(Receipt&& rhs)
{
    flag = rhs.flag;
    message = rhs.message;
    future = std::move(rhs.future);
    return *this;
}


bool Receipt::submitted() const
{
    return (flag == 0);
}


bool Receipt::ready() const
{
    py_lock.lock();
    bool z = future.attr("ready")().cast<bool>();
    py_lock.unlock();
    return z;
}


long Receipt::result()
{
    py_lock.lock();
    py::tuple z = future.attr("get")();
    long zz = z[0].cast<long>();
    py_lock.unlock();
    return zz;
}


Driver::Driver()
{
    Py_Initialize();
}


void Driver::initialize(
    std::string const & model_config_json,
    std::vector<std::string> const & float_feature_names,
    std::vector<std::string> const & str_feature_names
    )
{
    auto driver_cls = py::module::import("py4cc4.py4cc").attr("Driver");
    _driver = driver_cls();

    auto kwargs = py::dict(
        py::arg("config_json") = py::cast(model_config_json),
        py::arg("float_feature_names") = float_feature_names,
        py::arg("str_feature_names") = str_feature_names
    );
    _driver.attr("initialize")(**kwargs);

    _initialized = true;
}


Receipt Driver::submit(
    std::vector<double> const & float_features,
    std::vector<std::string> const & str_features,
    const int int_feature
    )
{
    py_lock.lock();
    auto kwargs = py::dict(
        py::arg("float_features") = float_features,
        py::arg("str_features") = str_features,
        py::arg("int_feature") = int_feature);

    py::object future = _driver.attr("submit")(**kwargs);

    int flag;
    std::string msg;
    if (future.is_none()) {
        flag = 1;
        msg = "System busy; resumit at a later time.";
    } else {
        flag = 0;
    }
    Receipt receipt(flag, msg, future);
    py_lock.unlock();

    return receipt;
}


void Driver::finalize()
{
    if (_initialized && !_finalized) {
        if (_driver.ptr() != nullptr) {
            _driver.attr("finalize")();
        }
        _finalized = true;
    }
}


Driver::~Driver()
{
    this->finalize();

    // Do not call Py_Finalize with pybind11.
    // Py_Finalize();
}
