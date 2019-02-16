import asyncio
from threading import Thread


class DelayQueue(object):
    __loop = asyncio.new_event_loop()

    def start(self):
        Thread(target=self._start_loop).start()

    def _start_loop(self):
        asyncio.set_event_loop(self.__loop)
        self.__loop.run_forever()

    def _call_later(self, delay, task, *args):
        self.__loop.call_later(delay, task, *args)

    def offer(self, delay, task, *args):
        self.__loop.call_soon_threadsafe(self._call_later, delay // 1000, task, *args)

    def shutdown(self):
        self.__loop.call_soon_threadsafe(self.__loop.stop)
