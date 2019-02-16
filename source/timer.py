from multiprocessing import Lock
from datetime import datetime

from .timing_wheel import TimingWheel
from .delay_queue import DelayQueue


class Timer(object):
    __lock = Lock()

    delay_queue = DelayQueue()
    task_counter = 0

    def __init__(self, tick_ms=1000, wheel_size=100, start_ms=datetime.now()):
        self.timing_wheel = TimingWheel(tick_ms=tick_ms, wheel_size=wheel_size, start_ms=start_ms)
        self.delay_queue.start()

    def add(self, timer_task_entry):
        with self.__lock:
            bucket, expiration_updated = self.timing_wheel.add(timer_task_entry)
            if bucket and expiration_updated:
                self.delay_queue.offer(bucket.expiration - self.timing_wheel.current_time, self.advance_clock, bucket)

    def advance_clock(self, bucket):
        if bucket:
            self.timing_wheel.advance_clock(time_ms=bucket.expiration)
            bucket.flush(self.add)
        return False

    def shutdown(self):
        self.delay_queue.shutdown()
