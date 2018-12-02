#ifndef CC4PY2_UTIL_H
#define CC4PY2_UTIL_H

#include <iostream>
#include <string>
#include <tuple>


void print(std::string const & msg=std::string())
{
    std::cout << msg << std::endl;
}


template<typename Map>
void print_map(const Map& m)
{
    std::cout << '{';
    auto i = 0;
    for(const auto& p: m) {
        if (i > 0) std::cout << ", ";
        std::cout << p.first << ':' << p.second;
        ++i;
    }
    std::cout << '}' << std::endl;
}


template<typename Vec>
void print_vec(const Vec& v)
{
    std::cout << '[';
    auto i = 0;
    for (const auto& p: v) {
        if (i > 0) std::cout << ", ";
        std::cout << p;
        ++i;
    }
    std::cout << ']' << std::endl;
}


#endif
