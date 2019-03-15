# coding: utf-8

from . import time_util


class TimerTaskEntry(object):
    """
    延时任务
    支持任务列表链表结构
    """
    # 前驱任务
    prev = None
    # 后继任务
    next = None

    def __init__(self, task, expiration=None, delay=None, *args, **kwargs):
        """
        初始化延时任务
        :param expiration: 过期时间
        :param task: 任务
        :param args:
        :param kwargs:
        """
        # 过期时间
        if expiration:
            # 直接指定过期时间优先
            self.expiration = expiration
        elif delay:
            # 指定延迟时间，换算为过期时间
            self.expiration = time_util.utc_now_timestamp_ms() + delay
        else:
            # 两者均未指定，默认为当前时间
            self.expiration = time_util.utc_now_timestamp_ms()
        self.task = task  # 任务
        self.args = args
        self.kwargs = kwargs
        self.cancelled = False  # 任务取消

    def cancel(self):
        """
        取消任务
        :return:
        """
        self.cancelled = True
