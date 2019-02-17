# coding: utf-8


class TimerTaskEntry(object):
    """
    延时任务
    支持任务列表链表结构
    """
    # 前驱任务
    prev = None
    # 后继任务
    next = None

    def __init__(self, expiration, task, *args, **kwargs):
        """
        初始化延时任务
        :param expiration: 过期时间
        :param task: 任务
        :param args:
        :param kwargs:
        """
        self.expiration = expiration  # 过期时间
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
