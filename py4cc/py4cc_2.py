# Second approach:
#   submit, no retrieve
# 'submit' returns 'async result' directly.

import copy
import json
import multiprocessing

from .common import run_big_model, Engine


class Driver(Engine):
    def submit(self, *, float_features, str_features, int_feature):
        assert len(self._float_feature_names) == len(float_features)
        assert len(self._str_feature_names) == len(str_features)
        try:
            if len(self._tasks) >= self._max_tasks:
                return None, ''

            result = self._pool.apply_async(
                run_big_model,
                kwds={'float_features': float_features,
                    'str_features': str_features,
                    'int_feature': int_feature},
            )

            return result, ''
        except:
            return None, traceback.format_exc()

