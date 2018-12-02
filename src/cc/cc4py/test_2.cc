#include "cc4py_2.h"
#include "test_common.h"
#include "pybind11/stl.h"

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
#include <tuple>
#include <vector>


//std::mutex cout_lock;


void do_one_thread(
    cc4py::Driver * driver,
    Datapoint const * data_in,
    long * data_out,
    int idx_from,
    int idx_to)
{
    for (int idx=idx_from; idx < idx_to; idx++) {
        long key = 0;
        while (1) {
            auto receipt = driver->submit(
                data_in[idx].float_features,
                data_in[idx].str_features,
                data_in[idx].int_feature
            );
            if (receipt.flag == 0) {
                key = receipt.key;
                break;
            } else {
                wait(1);
            }
        }
        if (key == 0) {
            data_out[idx] = -1;
            continue;
        }
        wait(1);

        while (1) {
            auto result = driver->retrieve(key);
            if (result.flag == 0) {
                data_out[idx] = result.value;
                break;
            } else {
                wait(1);
            }
        }
    }
}


int main(int const argc, char const * const * const argv)
{
    do_threads<cc4py::Driver>(do_on_thread);
    return 0;
}
