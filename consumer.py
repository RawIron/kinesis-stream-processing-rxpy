import itertools
import random
import string
from time import strftime, gmtime
from Queue import Queue

import inject
import fromqueue
from rx import Observable, Observer



class EventWriter(Observer):
  pass


class ConsoleEventWriter(EventWriter):
  def on_next(self, x):
    print x
  def on_error(self, x):
    print x
  def on_completed(self):
    pass


class GroupCounter(Observer):
  def on_next(self, events):
    events \
      .map(lambda event: (event[0], 1)) \
      .reduce(lambda acc, x: (x[0], acc[1] + x[1])) \
      .subscribe(ConsoleEventWriter())

  def on_error(self, x):
    print x

  def on_completed(self):
    pass


def group_timeout():
  return 64000


def key_builder():
  pass


def create_timestamp_key():

  def timestamp_key(event):
    return (strftime("%Y%m%d%H%M", gmtime()), event)

  return timestamp_key


def create_random_key():

  def random_key(event):
    return (random.randint(0,1000), event)

  return random_key


def create_single_key():

  def single_key(event):
    return ('one-key', event)

  return single_key


class Stream(Observable):
  pass


def infinite_stream():
  return Observable.from_iterable(itertools.count())


def finite_queue():
  q = Queue()
  for item in range(100):
    q.put(item)
  return Observable.from_queue(q)


def finite_list():
  return Observable.from_iterable([item for item in range(100)])


def finite(binder):
    binder.bind_to_provider(Stream, finite_queue)
    binder.bind(EventWriter, ConsoleEventWriter())
    binder.bind_to_provider(key_builder, create_random_key)


def infinite_base(binder):
    binder.bind_to_provider(Stream, infinite_stream)
    binder.bind(EventWriter, ConsoleEventWriter())


def infinite(binder):
    infinite_base(binder)
    binder.bind_to_provider(key_builder, create_timestamp_key)


def infinite_random(binder):
    infinite_base(binder)
    binder.bind_to_provider(key_builder, create_random_key)


def infinite_single(binder):
    infinite_base(binder)
    binder.bind_to_provider(key_builder, create_single_key)


inject.configure(finite)


events = inject.instance(Stream)

events \
  .map(inject.instance(key_builder)) \
  .group_by_until(
    lambda event: event[0],
    None,
    lambda x: Observable.timer(group_timeout()),
    None
  ) \
  .subscribe(GroupCounter())

