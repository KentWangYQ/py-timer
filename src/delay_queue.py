# coding: utf-8

import asyncio
from threading import Thread


class DelayQueue(object):
    """
    延时队列
    由asyncio的event loop驱动
    """
    __loop = asyncio.new_event_loop()

    def _start_loop(self):
        """
        启动event loop
        :return:
        """
        asyncio.set_event_loop(self.__loop)
        self.__loop.run_forever()

    def start(self):
        """
        启动队列
        由于asyncio的event loop需要block整个线程，所以新起一个线程来专门跑event loop
        :return:
        """
        Thread(target=self._start_loop).start()

    def offer(self, delay, task, *args, **kwargs):
        """
        向队列中添加任务
        :param delay: 延时时间
        :param task: 任务
        :param args:
        :param kwargs:
        :return:
        """
        self.__loop.call_soon_threadsafe(self.__loop.call_later, delay // 1000, task, *args, **kwargs)

    def shutdown(self):
        """
        关闭队列
        通过loop的线程安全方法，安全的关闭队列
        :return:
        """
        self.__loop.call_soon_threadsafe(self.__loop.stop)
