import itertools
import random
import string

import inject
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


class Stream(Observable):
  pass


def infinite_stream():
  return Observable.from_iterable(itertools.count())


def file_stream():
  return Observable.from_iterable(open("GDELT-MINI.TSV"))


def file(binder):
    binder.bind_to_provider(Stream, file_stream)
    binder.bind(EventWriter, ConsoleEventWriter())
    binder.bind_to_provider(event_builder, create_gdelt_event)

def infinite(binder):
    binder.bind_to_provider(Stream, infinite_stream)
    binder.bind(EventWriter, ConsoleEventWriter())
    binder.bind_to_provider(event_builder, create_random_event)


inject.configure(file)


raw_events = inject.instance(Stream)

raw_events \
  .map(inject.instance(event_builder)) \
  .subscribe(inject.instance(EventWriter))

