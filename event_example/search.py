# Copyright LGPL by Christopher Angell

from tkinter import Listbox, StringVar, Toplevel, ttk

from .events import FetchEvent, SearchEvent, SearchResultEvent

class SearchWindow:

    def __init__(self, root, eventbus):
        self._eventbus = eventbus

        t = Toplevel(root)
        
        ttk.Label(t, text="Query").grid(column=0, row=0)

        self._query = StringVar()
        ttk.Entry(t, textvariable=self._query).grid(column=1, row=0)

        button = ttk.Button(t, text="Search", command=self.submit)
        button.grid(column=2, row=0, sticky='nwes')

        
        self._results = StringVar()
        self._listbox = Listbox(t, listvariable=self._results, height=5)
        self._listbox.grid(column=0, row=1, columnspan=3, sticky='nwes')
        self._listbox.bind('<<ListboxSelect>>', self.fetch)

        eventbus.connect(SearchResultEvent, self.receive)

    def submit(self, *args):
        self._eventbus.emit(SearchEvent(self._query.get()))

    def receive(self, event):
        self._results.set(event.data)

    def fetch(self, *args):
        try:
            index = self._listbox.curselection()[0]
        except IndexError:
            return
        name = self._listbox.get(index)
        self._eventbus.emit(FetchEvent(name))
