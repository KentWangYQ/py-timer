# coding: utf-8

from multiprocessing import Lock

from .timer_task_entry import TimerTaskEntry


class TimerTaskList(object):
    """
    延时任务列表，为双向链表结构
    """
    __lock = Lock()

    # 过期时间
    _expiration = -1

    @property
    def expiration(self):
        with self.__lock:
            return self._expiration

    @expiration.setter
    def expiration(self, value):
        with self.__lock:
            self._expiration = value

    # 任务计数器
    _task_counter = 0

    @property
    def task_counter(self):
        with self.__lock:
            return self._task_counter

    def __init__(self, expiration=0):
        """
        初始化延时任务列表
        :param expiration:
        """
        '''
        链表root为哨兵，不包含任务，便于处理边界
        '''
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
        """
        获取过期时间
        :return:
        """
        return self.expiration

    def add(self, timer_task_entry):
        """
        添加任务
        :param timer_task_entry:
        :return:
        """
        with self.__lock:
            tail = self.root.prev
            timer_task_entry.next = self.root
            timer_task_entry.prev = tail
            tail.next = timer_task_entry
            self.root.prev = timer_task_entry
            self._task_counter += 1

    def remove(self, timer_task_entry):
        """
        删除任务
        :param timer_task_entry:
        :return:
        """
        with self.__lock:
            timer_task_entry.next.prev = timer_task_entry.prev
            timer_task_entry.prev.next = timer_task_entry.next
            timer_task_entry.next = None
            timer_task_entry.prev = None
            self._task_counter -= 1

    def flush(self, func):
        """
        刷新任务列表，将所有任务删除，然后依次调用参数func来处理任务
        :param func: 任务处理函数
        :return:
        """
        head = self.root.next
        self.root.next = self.root
        self.root.prev = self.root
        while head is not self.root:
            _next = head.next
            self.remove(head)
            func(head)
            head = _next

        # 充值任务列表过期时间
        self.expiration = -1
