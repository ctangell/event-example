# © Copyright 2022 Christopher Angell
# All rights reserved
# This software is licensed under the terms of the LGPL included in LICENSE.txt

from tkinter import Tk

from .eventbus import EventBus
from .db import Db
from .result import ResultWindow
from .search import SearchWindow

# get the root window
root = Tk()
# create the event bus - it depends on Tk since it needs to move events to the
# main thread to provide a thread-safe emit
eventbus = EventBus(root)
# Note how the database, search window, and result window do not depend on each
# other, they depend only on the event bus
db = Db(eventbus)
search = SearchWindow(root, eventbus)
result = ResultWindow(root, eventbus)
# start the main loop
root.mainloop()