import time

from pycc.cpp_1 import Driver
from .common import do_threads


def do_one_thread(driver, data, results, idx_from, idx_to):
    for idx in range(idx_from, idx_to):
        while True:
            key, msg = driver.submit(**data[idx])
            if key is None:
                if msg == '':
                    time.sleep(0.001)
                else:
                    raise Exception(msg)
            else:
                break

        time.sleep(0.001)

        while True:
            val, msg = driver.retrieve(key)
            if val is None:
                if msg == '':
                    time.sleep(0.001)
                else:
                    raise Exception(msg)
            else:
                results[idx] = val
                break


def test():
    do_threads(Driver, do_one_thread)


