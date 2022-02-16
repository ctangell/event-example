# Copyright LGPL by Christopher Angell

from collections import namedtuple

Event = namedtuple("Event", ["data"])

class SearchEvent(Event):
    """ data: str
        the sub-string to look for in the names
    """
    pass

class SearchResultEvent(Event):
    """ data: list[str]
        list of names of found items
    """
    pass

class FetchEvent(Event):
    """ data: str
        name of item to fetch
    """
    pass

class FetchResultEvent(Event):
    """ data: item
        the full item that has been fetched
    """
    pass

class UpdateEvent(Event):
    """ data: tuple(name: str, color: str, quantity: int)
        the items data to update in the record 
    """