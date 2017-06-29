#include "cc4py_1.h"

#include "Python.h"

#include <algorithm>
#include <cassert>
#include <exception>
#include <iostream>
#include <memory>


using namespace cc4py;

std::string py_module_name = "py4cc.py4cc_1";


PyObject* to_py_float_list(double const * buffer, const int n)
{
    PyObject* list = PyList_New((Py_ssize_t) n);
    for (Py_ssize_t i = 0; i < n; i++) {
        PyList_SetItem(list, i, PyFloat_FromDouble(buffer[i]));
    }
    return list;
}


PyObject* to_py_str_list(char const * const* buffer, int n)
{
    PyObject* list = PyList_New((Py_ssize_t) n);
    for (Py_ssize_t i = 0; i < n; i++) {
        PyList_SetItem(list, i, PyUnicode_FromString(buffer[i]));
    }
    return list;
}


std::vector<char const *> to_c_strs(std::vector<std::string> const& strings)
{
    std::vector<char const *> c_strs;
    c_strs.reserve(strings.size());
    std::transform(std::begin(strings), std::end(strings),
        std::back_inserter(c_strs), std::mem_fn(&std::string::c_str));
    return c_strs;
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
    auto pModule = PyImport_Import(PyUnicode_FromString(py_module_name.c_str()));
    auto driver_cls = PyObject_GetAttrString(pModule, "Driver");

    auto noargs = PyTuple_New(0);

    _driver = PyObject_Call(driver_cls, noargs, nullptr);

    auto kwargs = PyDict_New();
    PyDict_SetItemString(kwargs, "config_json", PyUnicode_FromString(model_config_json.c_str()));
    PyDict_SetItemString(kwargs, "float_feature_names",
        to_py_str_list(to_c_strs(float_feature_names).data(), float_feature_names.size()));
    PyDict_SetItemString(kwargs, "str_feature_names",
        to_py_str_list(to_c_strs(str_feature_names).data(), str_feature_names.size()));

    auto method = PyObject_GetAttrString(_driver, "initialize");
    PyObject_Call(method, noargs, kwargs);

    _initialized = true;
}


long Driver::submit(
    std::vector<double> const & float_features,
    std::vector<std::string> const & str_features,
    const int int_feature
    )
{
    auto method = PyObject_GetAttrString(_driver, "submit");

    auto kwargs = PyDict_New();
    PyDict_SetItemString(kwargs, "float_features", to_py_float_list(float_features.data(), float_features.size()));
    PyDict_SetItemString(kwargs, "str_features", to_py_str_list(to_c_strs(str_features).data(), str_features.size()));
    PyDict_SetItemString(kwargs, "int_feature", PyLong_FromLong(int_feature));

    auto args = PyTuple_New(0);

    auto z = PyObject_Call(method, args, kwargs);
    auto key = PyTuple_GetItem(z, 0);
    auto msg = PyTuple_GetItem(z, 1);

    if (key == Py_None) {
        assert(PyUnicode_GET_LENGTH(msg) == 0);
        return -1;  // capacity reached; not accepting submissions.
    } else {
        return PyLong_AsLong(key);
    }
}


long Driver::retrieve(const long key)
{
    auto method = PyUnicode_FromString("retrieve");
    auto py_key = PyLong_FromLong(key);
    auto z = PyObject_CallMethodObjArgs(_driver, method, py_key, nullptr);

    auto val = PyTuple_GetItem(z, 0);
    auto msg = PyTuple_GetItem(z, 1);

    if (val == Py_None) {
        assert(PyUnicode_GET_LENGTH(msg) == 0);
        return -1;    // not ready yet.
    } else {
        return PyLong_AsLong(val);
    }
}


void Driver::finalize()
{
    if (_initialized && !_finalized) {
        if (_driver) {
            PyObject_CallMethod(_driver, "finalize", nullptr);
        }
        _finalized = true;
    }
}


Driver::~Driver()
{
    this->finalize();
    Py_Finalize();
}
