import itertools
import random
import string

from rx import Observable, Observer


class Writer(Observer):
  pass


class ConsoleEventWriter(Writer):
  def on_next(self, x):
    print x
  def on_error(self, x):
    print x
  def on_completed(self):
    pass


def create_random_event(x):
  N = 32
  alphabet = string.ascii_uppercase + string.digits

  return {"id": x, "data": ''.join(random.choice(alphabet) for _ in range(N))}


def infinite_stream():
  return Observable.from_iterable(itertools.count())


raw_events = infinite_stream()

raw_events \
  .map(create_random_event) \
  .subscribe(ConsoleEventWriter())
