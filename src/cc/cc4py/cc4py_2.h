#ifndef CC4PY_H_
#define CC4PY_H_

#include "Python.h"
#include "pybind11/pybind11.h"

#include <string>
#include <vector>


namespace py = pybind11;


namespace cc4py {
    class TaskReceipt {
        private:
            int _flag;
                // 0 -- success; come query the result later with `retrieve`.
                // 1 -- system is full with tasks; try re-submit later.
                // 2+ -- error.
            long _key;
                // This is a valid, positive key when `flag` is `0`, to identify the task just submitted.
                // It is going to be used later to request result of this particular task.
            std::string _message;
                // Message when `flag` is nonzero.
        public:
            TaskReceipt(py::object, std::string const &);
            bool successful() const;
            bool delayed() const;
            bool failed() const;
            std::string const & error_message() const;
    };


    class TaskResult {
        private:
            int _flag;
                //  0 -- success; this task is removed from the system;
                //       the caller should use the returned `value`.
                //  1 -- the requested task is unfinished; try again later.
                //  2+ -- error; this task is removed from the system; the caller should move on.
            long _value;
                // Usually this is a valid positive number only when `flag` is `0`.
            std::string _message;
                // Empty if all is well; otherwise inspect and log this message unless `flag` is `1`.
        public:
            TaskResult(py::object, std::string const &);
            bool successful() const;
            bool delayed() const;
            bool failed() const;
            long value() const;
            std::string const & error_message() const;
    };


    class Driver
    {
    private:
        py::object _driver;
        bool _initialized = false;
        bool _finalized = false;

    public:
        Driver();

        void initialize(
            std::string const & config_json,
            std::vector<std::string> const & float_feature_names,
            std::vector<std::string> const & str_feature_names
            );

        TaskReceipt submit(
            std::vector<double> const & float_features,
            std::vector<std::string> const & str_features,
            const int int_feature
            );

        TaskResult retrieve(TaskReceipt const &);

        void finalize();

        ~Driver();
    };

}   // namespace

#endif  // CC4PY_H_
