#ifndef CC4PY_H_
#define CC4PY_H_

#include "Python.h"

#include <string>
#include <vector>


namespace cc4py {

    class Driver
    {
    private:
        PyObject * _driver = nullptr;

        bool _initialized = false;
        bool _finalized = false;

    public:
        Driver();

        void initialize(
            std::string const & config_json,
            std::vector<std::string> const & float_feature_names,
            std::vector<std::string> const & str_feature_names
            );

        long submit(
            std::vector<double> const & float_features,
            std::vector<std::string> const & str_features,
            const int int_feature
            );

        long retrieve(const long key);

        void finalize();

        ~Driver();
    };

}   // namespace

#endif  // CC4PY_H_
