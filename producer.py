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


def create_gdelt_event(x):
  headers = ["Date", "Source", "Target", "CAMEOCode", "NumEvents", "NumArts", "QuadClass", "Goldstein",
             "SourceGeoType", "SourceGeoLat", "SourceGeoLong",
             "TargetGeoType", "TargetGeoLat", "TargetGeoLong",
             "ActionGeoType", "ActionGeoLat", "ActionGeoLong"]
  return dict(zip(headers, x.replace("\n", "").split("\t")))


def file_stream():
  return Observable.from_iterable(open("GDELT-MINI.TSV"))


def create_event(x):
  return create_gdelt_event(x)


def stream():
  return file_stream()


raw_events = stream()

raw_events \
  .map(create_event) \
  .subscribe(ConsoleEventWriter())

