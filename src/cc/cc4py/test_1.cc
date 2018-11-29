#include "cc4py_1.h"
#include "test_common.h"

#include <cassert>
#include <chrono>
#include <cmath>
#include <exception>
#include <iostream>
#include <memory>
#include <mutex>
#include <random>
#include <string>
#include <thread>
#include <vector>


std::mutex py_lock;
//std::mutex cout_lock;



Datapoint make_point(
    double x, double y, double z,
    std::string a, std::string b,
    long k)
{
    return std::move(
        Datapoint{
            std::vector<double>{x, y, z},
            std::vector<std::string>{a, b},
            k
        }
    );
}


std::vector<Datapoint> make_data(uint n)
{
    std::vector<Datapoint> data;
    data.push_back(make_point(1.1, 11.2, .3, "ab", "cda", 27));
    data.push_back(make_point(2.3, 1.23, 11.3, "abc", "csd", 29));
    data.push_back(make_point(1.88, 51.2, 1.34, "attb", "cdvfsdfv", 7));
    data.push_back(make_point(1.1, 33.2, 1.003, "ab", "cdv11", 127));
    data.push_back(make_point(10.1, 1.2, 2.3, "ab0", "cda88", 270));
    data.push_back(make_point(1.223, 21.2, 3.3, "abcsdf", "cd6", 129));
    data.push_back(make_point(0.88, 1.02, 10.3, "atewwtb", "cd34vv", 72));
    data.push_back(make_point(3.1, 33.2, 4.3, "abaer", "cdaav", 17));
    assert(n == data.size());
    return data;
}


int answer(const Datapoint & dp)
{
    int z = static_cast<int>(
        fabs(dp.float_features[0]) +
        fabs(dp.float_features[1]) +
        fabs(dp.float_features[2]));
    z += dp.str_features[0].size() + dp.str_features[1].size();
    z += dp.int_feature;
    z = z % 100000;
    return z;
}


void do_one_thread(
    cc4py::Driver * driver,
    Datapoint const * data_in,
    int * data_out,
    int idx_from,
    int idx_to)
{
    for (int idx=idx_from; idx < idx_to; idx++) {
        long key = 0;
        while (1) {
            py_lock.lock();
            key = driver->submit(
                data_in[idx].float_features,
                data_in[idx].str_features,
                data_in[idx].int_feature
            );
            py_lock.unlock();
            if (key <= 0) {
                wait();
            } else {
                break;
            }
        }

        wait();

        while (1) {
            py_lock.lock();
            long result = driver->retrieve(key);
            py_lock.unlock();
            if (result <= 0) {
                wait();                
            } else {
                data_out[idx] = result;
                break;
            }
        }
    }
}


int main(int const argc, char const * const * const argv)
{
    int N = 8;
    auto dataset = make_data(N);

    int NTHREADS = 2;
    int idx_from[NTHREADS] = {0, 4};
    int idx_to[NTHREADS] = {4, N};

    std::vector<int> results(N);

    cc4py::Driver driver;

    driver.initialize(
        "{\"a\": 38, \"b\": [2, 3, 4]}",
        std::vector<std::string>{"float1", "float2", "float3"},
        std::vector<std::string>{"str1", "str2"}
    );

    std::vector<std::thread> cc_threads(NTHREADS);
    for (int i=0; i < NTHREADS; i++) {
        cc_threads[i] = std::thread(
            do_one_thread,
            &driver,
            dataset.data(),
            results.data(),
            idx_from[i],
            idx_to[i]);
    }
    for (auto it=cc_threads.begin(); it != cc_threads.end(); ++it) {
        it->join();
    }

    driver.finalize();

    for (int i = 0; i < N; ++i) {
        assert(answer(dataset[i]) == results[i]);
    }

    return 0;
}
