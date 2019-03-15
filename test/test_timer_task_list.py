# -*- coding: utf-8 -*-

import unittest

from src import time_util
from src.timer_task_entry import TimerTaskEntry
from src.timer_task_list import TimerTaskList


class TimerTaskListTest(unittest.TestCase):
    def test_task_counter(self):
        ttl = TimerTaskList()
        c = 5
        for _ in range(c):
            ttl.add(TimerTaskEntry(expiration=time_util.utc_now_timestamp_ms(), task=lambda: None))

        self.assertEqual(c, ttl.task_counter, 'The task_counter has wrong number!')
