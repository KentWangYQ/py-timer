# coding: utf-8

from datetime import datetime


class TimerTaskEntry(object):
    def __init__(self, task, expiration_ms=0):
        self.task = task
        self.expiration_ms = expiration_ms
        self.cancelled = False

    def cancel(self):
        self.cancelled = True


class TimerTaskList(list):
    def __init__(self, expiration_ms=0):
        assert expiration_ms >= 0, 'expiration_ms must gte 0!'
        super().__init__()
        self.expiration_ms = expiration_ms

    def set_expiration_ms(self, expiration_ms):
        """
        设置expiration_ms值，并新值与原值是否相等。
        如果不相等，返回True，反之返回False。
        :param expiration_ms:
        :return:
        """
        assert expiration_ms >= 0, 'expiration_ms must gte 0!'

        prev, self.expiration_ms = self.expiration_ms, expiration_ms
        return prev != expiration_ms


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
        self.buckets = [TimerTaskList()] * self.wheel_size  # Type: [TimerTaskList]

    def add(self, timer_task_entry):
        """
        往时间轮中添加新任务
        :param timer_task_entry:
        :return:
        """
        if timer_task_entry.expiration_ms < self.current_time + self.tick_ms:
            '''
            任务已过期
            '''
            # TODO: 执行task
            # task_executor.submit(timer_task_entry.task)
            pass
        elif timer_task_entry.delay < self.current_time + self.interval:
            '''
            任务过期时间在本时间轮跨度内
            '''
            # 计算task应存入的轮槽索引值
            idx = timer_task_entry.delay // self.tick_ms % self.wheel_size
            # 找到对应轮槽
            bucket = self.buckets[idx]
            # 向轮槽中的timer_task_list增加task
            # TODO: bucket需要与delay_queue共享，考虑写入时是否需要加锁
            bucket.append(timer_task_entry)
            # 设置轮槽过期时间
            if bucket.set_expiration_ms(idx * self.tick_ms):
                # 如果过期时间变动，向delay_queue注册timer_task_list
                # TODO: 向delay_queue注册timer_task_list
                # queue.offer(bucket)
                pass
        else:
            '''
            任务过期时间不在本时间轮跨度内
            '''
            if not self.overflow_wheel:
                # 创建高阶时间轮
                self.add_overflow_wheel()

            # 向高阶时间轮添加任务
            self.overflow_wheel.add(timer_task_entry=timer_task_entry)

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

            # TODO: 考虑降级操作
