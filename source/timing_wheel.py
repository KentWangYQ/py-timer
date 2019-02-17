# coding: utf-8

from datetime import datetime

from .timer_task_list import TimerTaskList


class TimingWheel(object):
    """
    时间轮
    """
    # 高阶时间轮
    overflow_wheel = None  # TimingWheel
    # 轮槽
    buckets = []

    def __init__(self, tick_ms=1000, wheel_size=100, start_ms=datetime.now()):
        """
        初始化时间轮
        :param tick_ms:
        :param wheel_size:
        :param start_ms:
        """
        # 开始时间，时间戳
        self.start_ms = start_ms  # Type: timestamp
        # 基本时间跨度，整数，单位：ms
        self.tick_ms = tick_ms  # Type: int
        # 时间轮容量(格数)
        self.wheel_size = wheel_size  # Type: int
        # 总体时间跨度，整数，单位：ms
        self.interval = self.tick_ms * self.wheel_size  # Type: int
        # 表盘指针，当前时间，tick_ms的整数倍
        self.current_time = 0  # Type: int
        # 初始化轮槽
        self.buckets = [TimerTaskList() for _ in range(self.wheel_size)]  # Type: [TimerTaskList]

    def add(self, timer_task_entry):
        """
        往时间轮中添加新任务
        :param timer_task_entry:
        :return:
        """
        if timer_task_entry.expiration < self.current_time + self.tick_ms:
            '''
            任务已过期
            '''
            # 执行task
            timer_task_entry.task(*timer_task_entry.args, **timer_task_entry.kwargs)
            return None, False
        elif timer_task_entry.expiration < self.current_time + self.interval:
            '''
            任务过期时间在本时间轮跨度内
            '''
            # 计算bucket index
            virtual_id = int(timer_task_entry.expiration // self.tick_ms)
            # 找到对应轮槽
            bucket = self.buckets[virtual_id % self.wheel_size]
            # 向轮槽中的timer_task_list增加task
            bucket.add(timer_task_entry)
            # 设置轮槽过期时间
            result = bucket.set_expiration(virtual_id * self.tick_ms)
            # 返回bucket和过期时间修改结果
            return bucket, result
        else:
            '''
            任务过期时间不在本时间轮跨度内
            '''
            if not self.overflow_wheel:
                # 创建高阶时间轮
                self.add_overflow_wheel()

            # 向高阶时间轮添加任务
            return self.overflow_wheel.add(timer_task_entry=timer_task_entry)

    def add_overflow_wheel(self):
        """
        创建高阶时间轮
        :return:
        """
        if not self.overflow_wheel:
            self.overflow_wheel = TimingWheel(tick_ms=self.interval, wheel_size=self.wheel_size, start_ms=self.start_ms)

    def advance_clock(self, time_ms):
        """
        推进时间轮
        :param time_ms:
        :return:
        """
        if time_ms >= self.current_time + self.tick_ms:
            # 推进时间轮指针
            self.current_time = time_ms - time_ms % self.tick_ms

            if self.overflow_wheel:
                # 推进高阶时间轮
                self.overflow_wheel.advance_clock(time_ms)
