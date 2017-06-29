# First approach:
#   submit/retrieve
# 'submit' returns 'key'.

import copy
import json
import multiprocessing
import traceback

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
                      'int_feature': int_feature
                      },
            )
            key = id(result)
            self._tasks[key] = result
            # A valid positive `key` occurs along with a flag of `0`.
            # key will have no collision because any key (i.e. memory address)
            # could be used again only after that result has been removed
            # from `_tasks`.

            return key, ''
        except:
            return None, traceback.format_exc()

    def retrieve(self, key):
        """
        Args:
            key: the key returned from `submit`, used to identify the particular task.

        Returns:
            tuple (flag, value, message).
                Usually `flag == 0` combined with `value > 0` is a sure sign of success.
        """
        try:
            result = self._tasks[key]
            if not result.ready():
                return None, ''
                # TODO: sometimes the first element here is a weird thing like
                # `(((((<NULL>, None, None), None, None), '', ''), '', '')`
                # Don't know how that happened.

            val, msg = result.get(0)
            del self._tasks[key]
            return val, msg
        except Exception as e:
            return None, traceback.format_exc()
