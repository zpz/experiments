#ifndef TEST_COMMON_H
#define TEST_COMMON_H

#include "pybind11/pybind11.h"

#include <cassert>
#include <chrono>
#include <iostream>
#include <random>
#include <string>
#include <thread>
#include <vector>


namespace py = pybind11;


struct Datapoint {
    std::vector<double> float_features;
    std::vector<std::string> str_features;
    long int_feature;

    void print() const {
        std:: cout << "Datapoint: {float_features: [";
        int idx = 0;
        for (const auto v : float_features) {
            if (idx > 0) std::cout << ", ";
            std::cout << v;
            idx++;
        }
        std::cout << "], str_features: [";
        idx = 0;
        for (const auto v : str_features) {
            if (idx > 0) std::cout << ", ";
            std::cout << '"' << v << '"';
            idx++;
        }
        std::cout << "], int_feature: " << int_feature << "}\n";
    }
};


std::vector<Datapoint> make_data()
{
    auto make_data = py::module::import("py4cc.tests.common").attr("makedata");
    py::list alldata = make_data();
    int n = alldata.attr("__len__")().cast<int>();
    std::vector<Datapoint> data(n);
    for (int idx=0; idx < n; ++idx) {
        py::dict d = py::dict(alldata[idx]);
        auto floats = d["float_features"].cast<std::vector<double>>();
        auto strs = d["str_features"].cast<std::vector<std::string>>();
        auto int_ = d["int_feature"].cast<long>();
        data[idx] = Datapoint{floats, strs, int_};
    }
    return data;
}


void wait(int millisec=1)
{
    std::this_thread::sleep_for(std::chrono::milliseconds(millisec));
}


template<typename Driver>
void do_threads(
        std::function<void(Driver *, Datapoint const *, long *, int, int)> do_one_thread
        )
{
    auto mtest = py::module::import("py4cc.tests.common");
    auto config_json = mtest.attr("config_json").cast<std::string>();
    auto float_feature_names = mtest.attr("float_feature_names").cast<std::vector<std::string>>();
    auto str_feature_names = mtest.attr("str_feature_names").cast<std::vector<std::string>>();

    Driver driver;
    driver.initialize(config_json, float_feature_names, str_feature_names);

    auto dataset = make_data();
    int N = dataset.size();

    std::vector<long> results(N);
    
    int n_threads = mtest.attr("n_threads").cast<int>();

    do_threads(n_threads, driver, dataset.data(), results.data(), N);


    int idx_from[n_threads];
    int idx_to[n_threads];
    idx_from[0] = 0;
    int last_to;
    for (int i=0; i < n_threads-1; i++) {
        last_to = N * (i+1) / n_threads;
        idx_to[i] = last_to;
        idx_from[i+1] = last_to;
    }
    idx_to[n_threads-1] = N;

    std::vector<std::thread> cc_threads(n_threads);
    for (int i=0; i < n_threads; i++) {
        cc_threads[i] = std::thread(
            do_one_thread,
            &driver,
            dataset.data(),
            results.data(),
            idx_from[i],
            idx_to[i]);
    }

    auto t1 = std::chrono::high_resolution_clock::now();
    for (auto it=cc_threads.begin(); it != cc_threads.end(); ++it) {
        it->join();
    }
    auto t2 = std::chrono::high_resolution_clock::now();

    auto millisec = std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count();
    std::cout << std::endl;
    std::cout << "total time: " << millisec / 1000. <<  " seconds" << std::endl;
    std::cout << "qps: " << static_cast<int>(N / (millisec / 1000.)) << std::endl;

    driver.finalize();

    auto big_model = py::module::import("py4cc.common").attr("big_model");

    for (int i = 0; i < N; ++i) {
        auto z = big_model(dataset[i].float_features, dataset[i].str_features,
                dataset[i].int_feature).cast<long>();
        assert(z == results[i]);
    }
}

#endif
