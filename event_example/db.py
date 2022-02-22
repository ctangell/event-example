# © Copyright 2022 Christopher Angell
# All rights reserved
# This software is licensed under the terms of the LGPL included in LICENSE.txt

from collections import namedtuple
from time import sleep

from .events import (
    FetchEvent, FetchResultEvent, SearchEvent, SearchResultEvent, UpdateEvent
)

Item = namedtuple("Item", ["name", "color", "quantity"])

class Db:
    """ Simple database simulating a key-value store. Listens and responds to
    events for searching, fetching, and updating.
    """

    def __init__(self, eventbus):
        # simulate a key-value store
        self._db = {
            "ketchup": Item("ketchup", "red", 2),
            "banana": Item("banana", "yellow", 5),
            "yogurt": Item("yogurt", "white", 1),
            "granola": Item("granola", "brown", 3),
        }
        # keep a reference to the event bus so that events can be emitted
        self._eventbus = eventbus
        # connect the methods to the given events
        eventbus.connect(SearchEvent, self.search, is_async=True)
        eventbus.connect(FetchEvent, self.fetch, is_async=True)
        eventbus.connect(UpdateEvent, self.update, is_async=True)

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
        # construct an item assuming the data is a tuple in-order
        item = Item(*event.data)
        # update the item in the database
        self._db[item.name] = item
    