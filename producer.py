import itertools
import random
import string
import multiprocessing as mp

import inject
from rx import Observable, Observer

import kinesis_writer as kinesis


# ReactiveX Observers
#
class EventWriter(Observer):
  pass


class ConsoleEventWriter(EventWriter):
  def on_next(self, x):
    print x
  def on_error(self, x):
    print x
  def on_completed(self):
    pass


class QueueEventWriter(EventWriter):
  def __init__(self, queue):
    self.event_queue = queue

  def on_next(self, x):
    self.event_queue.put(x)

  def on_error(self, x):
    print x

  def on_completed(self):
    pass


class KinesisEventWriter(EventWriter):
  def __init__(self, write_func):
    self.write = write_func

  def on_next(self, x):
    self.write(x)

  def on_error(self, x):
    print x

  def on_completed(self):
    pass


# Event Builders
#
def event_builder():
  pass


def create_random_event():

  def random_event(x):
    N = 32
    alphabet = string.ascii_uppercase + string.digits

    return {"id": x, "data": ''.join(random.choice(alphabet) for _ in range(N))}

  return random_event


def create_gdelt_event():

  def gdelt_event(x):
    headers = ["Date", "Source", "Target", "CAMEOCode", "NumEvents", "NumArts", "QuadClass", "Goldstein",
               "SourceGeoType", "SourceGeoLat", "SourceGeoLong",
               "TargetGeoType", "TargetGeoLat", "TargetGeoLong",
               "ActionGeoType", "ActionGeoLat", "ActionGeoLong"]
    return dict(zip(headers, x.replace("\n", "").split("\t")))

  return gdelt_event


# In-Streams
#
class Stream(Observable):
  pass


def infinite_stream():
  return Observable.from_iterable(itertools.count())


def file_stream():
  return Observable.from_iterable(open("GDELT-MINI.TSV"))


def finite_list():
  return Observable.from_iterable([item for item in range(100)])


# Injector
#
def file_base(binder):
  binder.bind_to_provider(Stream, file_stream)
  binder.bind_to_provider(event_builder, create_gdelt_event)


def file(binder):
  file_base(binder)
  binder.bind(EventWriter, ConsoleEventWriter())


def file_to_queue(binder):
  file_base(binder)
  queue = mp.Queue()
  binder.bind(EventWriter, QueueEventWriter(queue))


def file_to_kinesis(binder):
  file_base(binder)
  region = 'us-west-2'
  stream = 'gdelt'
  key_func = lambda x: x['Target']
  binder.bind(EventWriter,
              KinesisEventWriter(kinesis.create_write(region, stream, key_func)))


def infinite(binder):
  binder.bind_to_provider(Stream, infinite_stream)
  binder.bind(EventWriter, ConsoleEventWriter())
  binder.bind_to_provider(event_builder, create_random_event)


# Generate Event Stream
#
def produce():
  raw_events = inject.instance(Stream)

  raw_events \
    .map(inject.instance(event_builder)) \
    .subscribe(inject.instance(EventWriter))


# MAIN
#
if __name__ == '__main__':

  inject.configure(file_to_kinesis)
  produce()

