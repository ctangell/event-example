# © Copyright 2022 Christopher Angell
# All rights reserved
# This software is licensed under the terms of the LGPL included in LICENSE.txt

from tkinter import Tk

from .eventbus import EventBus
from .db import Db
from .result import ResultWindow
from .search import SearchWindow

root = Tk()
eventbus = EventBus(root)
db = Db(eventbus)
search = SearchWindow(root, eventbus)
result = ResultWindow(root, eventbus)
root.mainloop()