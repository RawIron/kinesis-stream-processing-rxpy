import sys, time
import json

from boto import kinesis


class KinesisException(Exception):
    pass


def _get_stream_status(conn, stream_name):
    r = conn.describe_stream(stream_name)
    description = r.get('StreamDescription')
    return description.get('StreamStatus')


def _wait_for_stream(conn, stream_name):
    SLEEP_TIME_SECONDS = 1

    status = _get_stream_status(conn, stream_name)
    while status != 'ACTIVE':
        time.sleep(SLEEP_TIME_SECONDS)
        status = _get_stream_status(conn, stream_name)


def create_write(region, stream_name, key_func):

    conn = kinesis.connect_to_region(region_name = region)

    try:
        status = _get_stream_status(conn, stream_name)
        if 'DELETING' == status:
            raise KinesisException('The stream: {s} is being deleted.'.format(s=stream_name))
        elif 'ACTIVE' != status:
            _wait_for_stream(conn, stream_name)
    except:
        raise KinesisException('The stream: {s} is being deleted.'.format(s=stream_name))

    def write(event):
        key = key_func(event)
        json_event = json.dumps(event)
        try:
            conn.put_record(stream_name, json_event, key)
        except Exception as e:
            raise KinesisException("Encountered an exception while trying to put: "
                             + event + " into stream: " + stream_name
                             + " exception was: " + str(e))

    return write
