#ifndef CC4PY_H_
#define CC4PY_H_

#include "Python.h"
#include "pybind11/pybind11.h"

#include <mutex>
#include <string>
#include <vector>


namespace py = pybind11;


namespace cc4py {
    // std::mutex py_lock;

    class Receipt
    {
        private:
            int flag = 1;
                // 0 -- success; come query the result later with `retrieve`.
                // 1 -- system is full with tasks; try re-submit later.
                // 2+ -- error.
            std::string message;
                // Message when `flag` is nonzero.
            py::object future;
                // This is a valid, positive key when `flag` is `0`, to identify the task just submitted.
                // It is going to be used later to request result of this particular task.

        public:
            Receipt();
            Receipt(int, std::string const &, py::object const &);
            Receipt(Receipt const &);
            Receipt& operator=(Receipt const &);
            Receipt& operator=(Receipt &&);
            bool submitted() const;
            bool ready() const;
            long result();
    };


    class Driver
    {
    private:
        bool _initialized = false;
        bool _finalized = false;

    public:
        py::object _driver;

        Driver();

        void initialize(
            std::string const & config_json,
            std::vector<std::string> const & float_feature_names,
            std::vector<std::string> const & str_feature_names
            );

        Receipt submit(
            std::vector<double> const & float_features,
            std::vector<std::string> const & str_features,
            const int int_feature
            );

        void finalize();

        ~Driver();
    };

}   // namespace

#endif  // CC4PY_H_
