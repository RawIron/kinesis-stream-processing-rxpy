from rx import Lock
from rx.core import Observable, AnonymousObservable
from rx.concurrency import current_thread_scheduler
from rx.internal import extensionclassmethod


@extensionclassmethod(Observable)
def from_queue(cls, queue, scheduler=None):

    scheduler = scheduler or current_thread_scheduler
    lock = Lock()

    def subscribe(observer):

        def action(action1, state=None):
          item = None
          with lock:
              # observer is completed fist time the queue is empty
              # not great but will do for now
              if not queue.empty():
                  item = queue.get()

          if item is not None:
              observer.on_next(item)
              action1(action)
          else:
              observer.on_completed()

        return scheduler.schedule_recursive(action)

    return AnonymousObservable(subscribe)
