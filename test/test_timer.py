# coding: utf-8

import unittest
import time
import math

from source.timer import Timer
from source.timer_task_entry import TimerTaskEntry


class TimerTest(unittest.TestCase):
    now = time.time()

    def _print(self, key):
        t = time.time() - self.now
        print('time: %s -- key: %s' % (round(t), key))
        self.assertLess(math.fabs(key - t), 1, 'error')

    def test_add(self):
        """
        添加任务测试
        :return:
        """
        timer = Timer(wheel_size=5)
        keys = [0, 0.1, 0.3, 0.8, 1, 2, 3, 4, 5, 8, 9, 10, 18, 24, 26, 30]
        for key in keys:
            timer.add(TimerTaskEntry(expiration=key * 1000, task=self._print, key=key))

        time.sleep(keys[-1])
        timer.shutdown()
