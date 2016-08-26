import Queue as StdQueue

from rx import Lock
from rx.core import Observable, AnonymousObservable
from rx.concurrency import current_thread_scheduler
from rx.internal import extensionclassmethod


@extensionclassmethod(Observable)
def from_queue(cls, mpqueue, scheduler=None):

    scheduler = scheduler or current_thread_scheduler
    lock = Lock()

    def subscribe(observer):

        def action(action1, state=None):
          with lock:

            try:
              # stream is completed
              # when no event was received for 3 sec
              item = mpqueue.get(True, 3)

              observer.on_next(item)
              action1(action)

            except StdQueue.Empty:
              observer.on_completed()

        return scheduler.schedule_recursive(action)

    return AnonymousObservable(subscribe)
