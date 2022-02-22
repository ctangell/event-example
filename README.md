# event-example
Example of an asynchronous event bus.  This example accompanies an article on
asynchronous event buses that appears [here]().

This example demonstrates the core mechanisms
needed to handle long-running tasks asynchronously in a desktop gui application,
namely the need to dispatch potentially long running events to separate threads,
and add an element to ensure that synchronous events are run from the main
thread. The later is accomplished by making the event bus emit function
thread-safe by moving the incoming events to the main thread via a queue and a
callback in the gui event loop that is triggered when an event is waiting in the
queue.

This example is written in Python, and  uses only Python standard library
components, so should be executable in any Python environment.

Library components used:

* tkinter - to model the GUI
* concurrent.Futures - to dispatch asynchronous handlers to a separate thread
* queue - a thread-safe queue to ferry events between threads
* namedtuple - as a convenient data structure that provides instantiation boilerplate

## How to run

To run, type in your terminal:

```bash
$ python -m event_example
```

Two windows should appear, a result window and a search window.  Run an empty
search in search window to get a list of results.  Click on a result and the
result will appear in the result window.  A two second delay is added to each
database operation to simulate a database query.  To see that this would cause
the app to momentarily freeze, change the lines in "event_example/db.py" that ¥
state `is_async=True` to `is_async=False`.  This will cause the app to become
unresponsive for two seconds with each database interaction.  This highlights
the importance of doing potentially blocking activities asynchronously in a gui
application.

## The code
