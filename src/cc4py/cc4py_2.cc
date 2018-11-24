#include "cc4py_2.h"

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

std::string py_module_name = "py4cc.py4cc_1";


TaskReceipt::TaskReceipt(py::object key, std::string const & msg)
{
    if (key.is_none()) {
        if (msg == "") {
            _flag = 1;
        } else {
            _flag = 2;
            _message = msg;
        }
    } else {
        _flag = 0;
        _key = key.cast<long>();
    }
}


bool TaskReceipt::successful() const {
    return _flag == 0;
}


bool TaskReceipt::delayed() const {
    return _flag == 1;
}


bool TaskReceipt::failed() const {
    return _flag == 2;
}


std::string const & TaskReceipt::error_message() const {
    return _message;
}


TaskResult::TaskResult(py::object result, std::string const & msg)
{
    if (result.is_none()) {
        if (msg == "") {
            _flag = 1;
        } else {
            _flag = 2;
            _message = msg;
        }
    } else {
        _flag = 0;
        _value = result.cast<long>();
    }
}


bool TaskResult::successful() const {
    return _flag == 0;
}


bool TaskResult::delayed() const {
    return _flag == 1;
}


bool TaskResult::failed() const {
    return _flag == 2;
}


std::string const & TaskResult::error_message() const {
    return _message;
}


long TaskResult::value() const {
    return _value;
}


Driver::Driver()
{
    // Initialize the Python interpreter.
    Py_Initialize();
}


void Driver::initialize(
    std::string const & model_config_json,
    std::vector<std::string> const & float_feature_names,
    std::vector<std::string> const & str_feature_names
    )
{
    auto driver_cls = py::module::import(py_module_name.c_str()).attr("Driver");
    _driver = driver_cls();

    auto kwargs = py::dict(
        py::arg("config_json") = py::cast(model_config_json),
        py::arg("float_feature_names") = float_feature_names,
        py::arg("str_feature_names") = str_feature_names
    );
    _driver.attr("initialize")(**kwargs);

    _initialized = true;
}


TaskReceipt Driver::submit(
    std::vector<double> const & float_features,
    std::vector<std::string> const & str_features,
    const int int_feature
    )
{
    py_lock.lock();

    auto kwargs = py::dict(
        py::arg("float_features") = float_features,
        py::arg("str_features") = str_features,
        py::arg("int_feature") = int_feature
        );

    py::object z = _driver.attr("submit")(**kwargs);

    auto result = TaskReceipt(z[0], z[1].cast<std::string>());

    py_lock.unlock();

    return result;
}


TaskResult Driver::retrieve(const long key)
{
    py_lock.lock();
    py::tuple z = _driver.attr("retrieve")(key);

    // Monitor for a wierd bug here.
    try {
        auto result = TaskResult(z[0], z[1].cast<std::string>());
        py_lock.unlock();
        return result;
    } catch (std::exception& e) {
        std::cout << "exception: " << e.what() << std::endl;
        std::cout << "z: " << std::endl << std::flush;
        py::print(z);
        std::cout << std::endl << std::flush;
        py_lock.unlock();
        throw;
    }
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
