import multiprocessing
import time
import traceback


def big_model(float_features, str_features, int_feature):
    z = int(sum(abs(v) for v in float_features))
    z += sum(len(s.upper()) for s in str_features)
    z += len([' '] * int_feature)
    z = z % 100000
    return z


def run_big_model(*, float_features, str_features, int_feature):
    try:
        z = big_model(float_features, str_features, int_feature)

        # Emulate a time consuming step,
        # but make the duration deterministic hence reproducible.
        time.sleep((z % 100 + 1) * 0.0001)

        return z, ''
    except Exception as e:
        return None, traceback.format_exc()


class Engine:
    def __init__(self):
        self._tasks = {}
        self._max_tasks = 64
        self._pool = None
        self._n_subprocesses = multiprocessing.cpu_count()

    def initialize(self, *, config_json, float_feature_names, str_feature_names):
        self._config_json = config_json
        self._float_feature_names = float_feature_names
        self._str_feature_names = str_feature_names

        self._pool = multiprocessing.Pool(
            self._n_subprocesses,
        )

        return self

    def finalize(self):
        pass
