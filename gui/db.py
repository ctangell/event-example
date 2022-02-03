# Copyright LGPL by Christopher Angell

from collections import namedtuple
from time import sleep

from .events import (
    FetchEvent, FetchResultEvent, SearchEvent, SearchResultEvent, UpdateEvent
)

Item = namedtuple("Item", ["name", "color", "quantity"])

class Db:

    def __init__(self, eventbus):
        # simulate a key-value store
        self._db = {
            "ketchup": Item("ketchup", "red", 2),
            "banana": Item("banana", "yellow", 5),
            "yogurt": Item("yogurt", "white", 1),
            "granola": Item("granola", "brown", 3),
        }
        self._eventbus = eventbus
        eventbus.handle(SearchEvent, self.search, is_async=True)
        eventbus.handle(FetchEvent, self.fetch, is_async=True)
        eventbus.handle(UpdateEvent, self.update, is_async=True)

    def search(self, event):
        sleep(2) # simulate long search time that would block the event loop
        results = [
            key for key in self._db.keys()
            if event.data in key
        ]
        # emit is thread-safe, will still run on main thread even if were on
        # a different thread 
        self._eventbus.emit(SearchResultEvent(results))

    def fetch(self, event):
        sleep(2) # simulate long fetch time that would block the event loop
        # emit is thread-safe, will still run on main thread even if were on
        # a different thread
        self._eventbus.emit(FetchResultEvent(self._db[event.data]))

    def update(self, event):
        sleep(2) # simulate long update time that would block the event loop
        item = Item(*event.data)
        self._db[item.name] = item
    