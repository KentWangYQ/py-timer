# coding: utf-8

import unittest
import time
import math
import random

from src.timer import Timer
from src.timer_task_entry import TimerTaskEntry


class TimerTest(unittest.TestCase):
    now = time.time()

    task_count = 0

    def _print(self, key):
        t = time.time() - self.now
        print('time: %s -- key: %s' % (round(t), key))
        self.assertLess(math.fabs(key - t), 1, 'error')
        self.task_count += 1

    def test_add(self):
        """
        添加任务测试
        :return:
        """
        timer = Timer(wheel_size=5)
        task = TimerTaskEntry(delay=10 * 1000, task=self._print, key=10)
        timer.add(task)
        task.cancel()

        keys = [0, 0.1, 0.3, 0.8, 1, 2, 3, 4, 5, 8, 9, 10, 18, 24, 26, 30]
        d = 0
        for i, key in enumerate(keys):
            r = random.randrange(0, 3)
            d += r
            keys[i] += d
            time.sleep(r)
            timer.add(TimerTaskEntry(delay=key * 1000, task=self._print, key=keys[i]))

        time.sleep(keys[-1])
        timer.shutdown()
