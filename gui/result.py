# Copyright LGPL by Christopher Angell

from tkinter import IntVar, StringVar, Toplevel, ttk

from .events import FetchResultEvent, UpdateEvent

class ResultWindow:

    def __init__(self, root, eventbus):
        self._eventbus = eventbus

        t = root

        ttk.Label(t, text="Name").grid(column=0, row=0)
        ttk.Label(t, text="Color").grid(column=0, row=1)
        ttk.Label(t, text="Quantity").grid(column=0, row=2)

        self._name = StringVar()
        ttk.Label(t, textvariable=self._name).grid(column=1, row=0)
        self._color = StringVar()
        ttk.Entry(t, textvariable=self._color).grid(column=1, row=1)
        self._quantity = StringVar()
        ttk.Entry(t, textvariable=self._quantity).grid(column=1, row=2)
        button = ttk.Button(t, text="Update", command=self.update)
        button.grid(column=0, row=3, columnspan=2)
        self._error = StringVar()
        errorlabel = ttk.Label(t, textvariable=self._error)
        errorlabel.grid(column=0, row=4, columnspan=2)

        eventbus.handle(FetchResultEvent, self.receive)

    def receive(self, event):
        self._name.set(event.data.name)
        self._color.set(event.data.color)
        self._quantity.set(str(event.data.quantity))

    def update(self, *args):
        try:
            quantity = int(self._quantity.get())
        except ValueError:
            self._error.set("Please enter int for quantity")
            return

        self._error.set("")
        name = self._name.get()
        color = self._color.get()
        self._eventbus.emit(UpdateEvent([name, color, quantity]))
