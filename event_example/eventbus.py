# © Copyright 2022 Christopher Angell
# All rights reserved
# This software is licensed under the terms of the LGPL included in LICENSE.txt

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from queue import SimpleQueue

class EventBus:
    """ The event bus that decouples the emitter of an event from the
    receiver of the event.  Allows registering a handler as an asynchronous
    handler which will then be run on a separate thread from the main thread.
    Moves incoming events always to the main thread to ensure that
    synchronous handlers which are usually gui-related will run on the main
    thread.
    """

    # the event signature for our custom trigger on the Tk event loop indicating
    # an event is waiting to be processed in the queue
    TK_SYNC_EVENT = "<<event-bus-trigger>>"

    def __init__(self, root):
        # the handlers are simply a mapping of event type to a list of handlers
        self._async_handlers = defaultdict(list)
        self._sync_handlers = defaultdict(list)
        # keep a reference to the Tk root as it's needed to trigger a handle on
        # the main thread
        self._root = root
        # the messaging mechanism to move events to the main thread is a queue
        # as all events are processed quickly we won't worry about problems
        # such as limiting the queue size
        self._queue = SimpleQueue()
        # our thread pool executor will use the default settings
        self._pool = ThreadPoolExecutor()

        # the custom event trigger needs to be registered with a handler in the
        # tk root
        root.bind(self.TK_SYNC_EVENT, self._emit)

    def emit(self, event):
        # thread safe emit
        # add the event to the queue
        self._queue.put(event)
        # trigger the tk event loop to let it know that an event bus event is
        # waiting
        self._root.event_generate(self.TK_SYNC_EVENT)

    def _emit(self, *args):
        # process the waiting events on the main thread
        while not self._queue.empty():
            # pop an event from the queue
            event = self._queue.get()
            # dispatch the event
            self.syncemit(event)

    def syncemit(self, event):
        # not thread safe
        # handle synchronous handlers first
        for handler in self._sync_handlers[type(event)]:
            try:
                # the handler will simply be executed, may want to send fail
                # events in case of failure
                handler(event)
            except Exception:
                pass

        # handle async handlers next
        for handler in self._async_handlers[type(event)]:
            # note we are not watching the status internally, just trusting that
            # the handler will execute correctly
            self._pool.submit(handler, event)

    def connect(self, eventcls, fn, is_async=False):
        # the function is added to the pertinent list. If worried about object
        # lifetimes, only weak references should be kept
        # priorities and filtering may also be warranted, which would need more
        # complicated structures than a simple dictionary with lists
        if is_async:
            self._async_handlers[eventcls].append(fn)
        else:
            self._sync_handlers[eventcls].append(fn)

    