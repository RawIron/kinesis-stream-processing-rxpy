class Bunch:
  def __init__(self, **kwds):
    self.__dict__.update(kwds)


KINESIS = Bunch(
  REGION = 'us-west-2',
  STREAM_NAME = 'gdelt',
)

PRODUCER = Bunch(
  FINITE_LIST_LEN = 100,
  GDELT_FILE = 'GDELT-MINI.TSV',
  RANDOM_EVENT_STR_LEN = 32,
)
