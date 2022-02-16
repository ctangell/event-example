# Copyright LGPL by Christopher Angell

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