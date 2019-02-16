class TimerTaskEntry(object):
    prev = None
    next = None

    def __init__(self, expiration, task, *args, **kwargs):
        self.expiration = expiration
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self.cancelled = False

    def cancel(self):
        self.cancelled = True
