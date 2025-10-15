# Kinesis as an Event Collector

Kinesis can be used as an Event Collector Service.
The clients, for example mobile devices, push events directly into a Kinesis Stream.

In this exercise the incoming events are generated from a file or randomly.


## Could AWS lambda functions be used?

To create quickly an implementation that comes with a lot of *production ready* features the *AWS lambda function* is worth a short look.
The question is though can *AWS lambda functions* do stream processing?

A *lambda function* triggered by events arriving in *Kinesis* get called with a batch of events.
The *lambda function* works on the event batch and returns the result.
The programming model is that for each batch of events a `lambda function` instance is created and after completion destroyed.

Thus stream processing is not a use-case for *lambda functions*.


## ReactiveX Python

Start with an implementation as simple as possible.

For the consumer use a small python script which reads from a downloaded file and writes line-by-line after being converted to an *event*.
Write the data into a *Kinesis* stream.

The consumer would be another simple python script.
Pull the events from the Kinesis stream.
Tag all events seen within a single minute with the same key value.
Next steps are a `groupUntil` with a defined *timeout* and the write of result to S3.

In case events should be counted by type and minute a composite key can be used. In Python use a tuple `((“usa”, “201608211700”), 1)`.

The events per minute per worker would be on S3 in real-time.


### Design

Simplest design consists of two modules.

1. The `producer`, which reads the data from the file sequentially.
Transforms TSV raw data into an event.
Creates a batch of event data.
Then pushes a batch into the Kinesis stream.

2. A `consumer`, which polls from the Kinesis stream.
Aggregates the event data.
And writes the result into persistent storage.


### Setup

use `virtualenvwrapper` and create a *virtual environment* for python.
```
mkvirtualenv streams
```

install the packages into the *virtual environment*
```
pip install -r requirements.txt
```

configure the AWS environment locally.
```
aws configure
```

create a Kinesis stream in AWS.
```
aws kinesis create-stream --stream-name <your-stream> --shard-count 1
```


### Run

#### Locally

run the producer and consumer in different processes connected by a queue
configure the consumer and producer via `inject` in `run_stream_processing.py`.

```
python run_stream_processing.py
```

producer can either generate infinite stream of random events or finite stream of events from a file.
it is possible to write the events to *console*, local queue or *Kinesis* stream.
change `inject.configure()` in `producer.py` to activate the suited configuration.

```
python producer.py
```

to test differently *keyed* (timestamp, random) events change `inject.configure()` in `consumer.py`.
running the consumer this way only makes sense if the process can connect to the configured stream, for example a *Kinesis Stream*.

```
python consumer.py
```
