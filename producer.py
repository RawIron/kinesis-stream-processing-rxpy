from __future__ import print_function

import itertools
import random
import string
import multiprocessing as mp

import inject
from rx import Observable, Observer

import settings
import kinesis_writer as kinesis


# ReactiveX Observers
#
class EventWriter(Observer):
  pass


class DefaultEventWriter(EventWriter):
  def __init__(self, write_func):
    self.write = write_func

  def on_next(self, x):
    self.write(x)

  def on_error(self, x):
    print(x)

  def on_completed(self):
    pass


def queue_create_write(mpqueue):
  return lambda x: mpqueue.put(x)


# Event Builders
#
def event_builder():
  pass


def create_random_event():

  def random_event(x):
    N = settings.PRODUCER.RANDOM_EVENT_STR_LEN

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
  gdelt_file = settings.PRODUCER.GDELT_FILE
  return Observable.from_iterable(open(gdelt_file))


def finite_list():
  SIZE = settings.PRODUCER.FINITE_LIST_LEN
  return Observable.from_iterable([item for item in range(SIZE)])


# Injector
#
def file_base(binder):
  binder.bind_to_provider(Stream, file_stream)
  binder.bind_to_provider(event_builder, create_gdelt_event)


def file_to_console(binder):
  file_base(binder)
  binder.bind(EventWriter, DefaultEventWriter(print))


def file_to_queue(binder):
  file_base(binder)
  queue = mp.Queue()
  binder.bind(EventWriter, DefaultEventWriter(queue_create_write(queue)))


def file_to_kinesis(binder):
  file_base(binder)
  region = settings.KINESIS.REGION
  stream = settings.KINESIS.STREAM_NAME
  key_func = lambda x: x['Target']
  binder.bind(EventWriter,
              DefaultEventWriter(kinesis.create_write(region, stream, key_func)))


def infinite_to_console(binder):
  binder.bind_to_provider(Stream, infinite_stream)
  binder.bind(EventWriter, DefaultEventWriter(print))
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

