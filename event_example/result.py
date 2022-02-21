# © Copyright 2022 Christopher Angell
# All rights reserved
# This software is licensed under the terms of the LGPL included in LICENSE.txt

from tkinter import StringVar, ttk

from .events import FetchResultEvent, UpdateEvent

class ResultWindow:
    """ Window to display a result.  Allows modification of the result and
    posting the update to the database by means of the event bus.
    """

    def __init__(self, root, eventbus):
        # save the event bus so events can be emitted later
        self._eventbus = eventbus

        # This window is the main window, so just use the root display
        t = root

        # add several labels for the result fields
        # 'grid' is necessary to get an item to actually display
        ttk.Label(t, text="Name").grid(column=0, row=0)
        ttk.Label(t, text="Color").grid(column=0, row=1)
        ttk.Label(t, text="Quantity").grid(column=0, row=2)

        # create display/edit fields for each of the result fields
        # the StringVar allows synching with the display
        self._name = StringVar()
        ttk.Label(t, textvariable=self._name).grid(column=1, row=0)
        self._color = StringVar()
        ttk.Entry(t, textvariable=self._color).grid(column=1, row=1)
        self._quantity = StringVar()
        ttk.Entry(t, textvariable=self._quantity).grid(column=1, row=2)
        # add a button to trigger an update
        button = ttk.Button(t, text="Update", command=self.update)
        button.grid(column=0, row=3, columnspan=2)
        # show validation error in case data is incorrect (quantity not int)
        self._error = StringVar()
        errorlabel = ttk.Label(t, textvariable=self._error)
        errorlabel.grid(column=0, row=4, columnspan=2)

        # connect the 'receive' function to handle the FetchResultEvent from db
        eventbus.connect(FetchResultEvent, self.receive)

    def receive(self, event):
        # event is FetchResultEvent
        self._name.set(event.data.name)
        self._color.set(event.data.color)
        self._quantity.set(str(event.data.quantity))

    def update(self, *args):
        # perform an update of the data
        try:
            # validate the entries first
            quantity = int(self._quantity.get())
        except ValueError:
            self._error.set("Please enter int for quantity")
            return

        # incase successful validation, clear the error
        self._error.set("")
        # fetch the other data from the display
        name = self._name.get()
        color = self._color.get()
        # trigger an update of the data
        # note: this doesn't block to prevent multiple updates while previous
        # updates are processing, but in production you would want to disable
        # the button until saving is done or another result is loaded
        self._eventbus.emit(UpdateEvent([name, color, quantity]))
