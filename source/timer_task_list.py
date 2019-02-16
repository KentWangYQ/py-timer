from multiprocessing import Lock

from .timer_task_entry import TimerTaskEntry


class TimerTaskList(object):
    __lock = Lock()

    _expiration = -1

    @property
    def expiration(self):
        with self.__lock:
            return self._expiration

    @expiration.setter
    def expiration(self, value):
        with self.__lock:
            self._expiration = value

    _task_counter = 0

    @property
    def task_counter(self):
        with self.__lock:
            return self._task_counter

    def __init__(self, expiration=0):
        self.root = TimerTaskEntry(expiration=None, task=None)
        self.root.prev = self.root
        self.root.next = self.root
        self.expiration = expiration

    def set_expiration(self, expiration):
        """
        设置expiration值，并新值与原值是否相等。
        如果不相等，返回True，反之返回False。
        :param expiration:
        :return:
        """
        prev, self.expiration = self.expiration, expiration
        return prev != expiration

    def get_expiration(self):
        return self.expiration

    def add(self, timer_task_entry):
        with self.__lock:
            tail = self.root.prev
            timer_task_entry.next = self.root
            timer_task_entry.prev = tail
            tail.next = timer_task_entry
            self.root.prev = timer_task_entry
            self._task_counter += 1

    def remove(self, timer_task_entry):
        with self.__lock:
            timer_task_entry.next.prev = timer_task_entry.prev
            timer_task_entry.prev.next = timer_task_entry.next
            timer_task_entry.next = None
            timer_task_entry.prev = None
            self._task_counter -= 1

    def flush(self, f):
        head = self.root.next
        self.root.next = self.root
        self.root.prev = self.root
        while head is not self.root:
            _next = head.next
            self.remove(head)
            f(head)
            head = _next

        self.expiration = -1
