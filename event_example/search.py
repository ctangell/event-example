# © Copyright 2022 Christopher Angell
# All rights reserved
# This software is licensed under the terms of the LGPL included in LICENSE.txt

from tkinter import Listbox, StringVar, Toplevel, ttk

from .events import FetchEvent, SearchEvent, SearchResultEvent

class SearchWindow:
    """ Window to conduct a search, and peruse abbreviated results. 
    Allows for selecting a result, and coordinating with the database and the
    result window through the event bus to load the result and display in result
    window.
    """

    def __init__(self, root, eventbus):
        # save the _eventbus as we need this to emit events later
        self._eventbus = eventbus

        # make a top level window
        t = Toplevel(root)
        
        # add a label to box, the grid is required to get the item to show
        ttk.Label(t, text="Query").grid(column=0, row=0)

        # a string var synchronizes with the display, entered value will be here
        self._query = StringVar()
        # add a text entry to the display
        ttk.Entry(t, textvariable=self._query).grid(column=1, row=0)

        # add a button to search, will call 'submit' when clicked
        button = ttk.Button(t, text="Search", command=self.submit)
        button.grid(column=2, row=0, sticky='nwes')

        # multi-line text fields also use StringVar
        self._results = StringVar()
        # create the list box, and show 5 items in it
        self._listbox = Listbox(t, listvariable=self._results, height=5)
        self._listbox.grid(column=0, row=1, columnspan=3, sticky='nwes')
        # the bind is necessary to react on a click in the list box
        self._listbox.bind('<<ListboxSelect>>', self.fetch)

        # register the 'receive' method as a handler for SearchResultEvent
        eventbus.connect(SearchResultEvent, self.receive)

    def submit(self, *args):
        # Conduct a search for the given query.
        # Search result will show up the listbox (see 'receive' below)
        self._eventbus.emit(SearchEvent(self._query.get()))

    def receive(self, event):
        # event is a SearchResultEvent
        # set the display to the search result
        self._results.set(event.data)

    def fetch(self, *args):
        # When an item is selected from the listbox, send an event to fetch the
        # full item.
        # The full item will show up in the result window. (see result.py)
        try:
            index = self._listbox.curselection()[0]
        except IndexError:
            return
        name = self._listbox.get(index)
        self._eventbus.emit(FetchEvent(name))
