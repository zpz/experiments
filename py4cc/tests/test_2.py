import time

from py4cc.py4cc_2 import Driver
from py4cc.tests.common import do_threads


def do_one_thread(driver, data, results, idx_from, idx_to):
    for idx in range(idx_from, idx_to):
        while True:
            future, msg = driver.submit(**data[idx])
            if future is None:
                if msg == '':
                    time.sleep(0.001)
                else:
                    raise Exception(msg)
            else:
                break

        time.sleep(0.001)

        while True:
            if future.ready():
                val, msg = future.get(0)
                if val is None:
                    raise Exception(msg)
                results[idx] = val
                break
            else:
                time.sleep(0.001)


if __name__ == '__main__':
    do_threads(Driver, do_one_thread)

