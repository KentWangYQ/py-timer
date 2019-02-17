# coding: utf-8

from multiprocessing import Lock
from datetime import datetime

from .timing_wheel import TimingWheel
from .delay_queue import DelayQueue


class Timer(object):
    """
    定时器
    支持延时和定时执行任务，任务列表右timing wheel管理，通过delay queue来驱动timing wheel.
    """
    __lock = Lock()

    # 延时队列
    delay_queue = DelayQueue()
    # 任务计数器
    task_counter = 0

    def __init__(self, tick_ms=1000, wheel_size=100, start_ms=datetime.now()):
        self.timing_wheel = TimingWheel(tick_ms=tick_ms, wheel_size=wheel_size, start_ms=start_ms)
        # 启动延时队列
        self.delay_queue.start()

    def add(self, timer_task_entry):
        """
        添加任务
        :param timer_task_entry:
        :return:
        """
        with self.__lock:
            # 向时间轮添加任务
            bucket, expiration_updated = self.timing_wheel.add(timer_task_entry)
            if bucket and expiration_updated:
                # 任务列表过期时间更新，向延时队列注册任务列表
                self.delay_queue.offer(bucket.expiration - self.timing_wheel.current_time, self.advance_clock, bucket)

    def advance_clock(self, bucket):
        """
        推进时间轮
        将时间轮推进到当前bucket的过期时间
        :param bucket:
        :return:
        """
        if bucket:
            # 推进时间轮
            self.timing_wheel.advance_clock(time_ms=bucket.expiration)
            # 刷新任务列表
            bucket.flush(self.add)

    def shutdown(self):
        """
        关闭定时器
        :return:
        """
        self.delay_queue.shutdown()
