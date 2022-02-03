# Copyright LGPL by Christopher Angell

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from queue import SimpleQueue

class EventBus:

    TK_SYNC_EVENT = "<<event-bus-trigger>>"

    def __init__(self, root):
        self._async_handlers = defaultdict(list)
        self._sync_handlers = defaultdict(list)
        self._root = root
        self._queue = SimpleQueue()
        self._pool = ThreadPoolExecutor()
        root.bind(self.TK_SYNC_EVENT, self._emit)

    def emit(self, event):
        # thread safe emit
        self._queue.put(event)
        self._root.event_generate(self.TK_SYNC_EVENT)

    def _emit(self, *args):
        while not self._queue.empty():
            event = self._queue.get()
            self.syncemit(event)

    def syncemit(self, event):
        # not thread safe
        # handle synchronous handlers first
        for handler in self._sync_handlers[type(event)]:
            try:
                handler(event)
            except Exception:
                pass

        # handle async handlers next
        for handler in self._async_handlers[type(event)]:
            self._pool.submit(handler, event)

    def handle(self, eventcls, fn, is_async=False):
        if is_async:
            self._async_handlers[eventcls].append(fn)
        else:
            self._sync_handlers[eventcls].append(fn)

    