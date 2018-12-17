import threading
import time

from faker import Faker
import numpy as np

from pycc.common import big_model


rnd_seed = 3333
sample_size = 640
n_threads = 16

config_json = '{"model_name": "time killer"}'
float_feature_names = ['value_1', 'value_2']
str_feature_names = ['name', 'sentence', 'id']


def makedata():
    N = sample_size
    fake = Faker()
    fake.seed(rnd_seed)

    data = [None] * N
    for idx in range(N):
        data[idx] = {
            'float_features': [fake.pyfloat(), fake.pyfloat()],
            'str_features': [fake.name(), fake.sentence(), fake.uuid4()],
            'int_feature': fake.pyint() % 1000
        }

    return data


def make_driver(driver_cls):
    driver = driver_cls()
    driver.initialize(config_json=config_json,
                      float_feature_names=float_feature_names,
                      str_feature_names=str_feature_names)
    return driver


def do_threads(driver_cls, do_one_thread):
    data = makedata()
    driver = make_driver(driver_cls)

    N = len(data)
    results = np.zeros(N, int)

    idx_from = [0] * n_threads
    idx_to = [N] * n_threads
    for i in range(n_threads - 1):
        last_to = N * (i+1) // n_threads
        idx_to[i] = last_to
        idx_from[i+1] = last_to

    threads = [
        threading.Thread(target=do_one_thread,
                         args=[driver, data, results, idx_from[i], idx_to[i]])
        for i in range(n_threads)
        ]

    time0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    time1 = time.perf_counter()

    driver.finalize()

    print('total time:', time1 - time0, 'seconds')
    print('processed', int(N / (time1 - time0)), 'cases per second')


    answers = np.array([big_model(**z) for z in data], int)
    assert all(results == answers)

