# Kinesis as an Event Collector

Kinesis can be used as an Event Collector Service.
The clients, for example mobile devices, push events directly into a Kinesis Stream.

## Synchronous, Blocking, Sequential

Simplest design consists of two modules.

1. The `producer`, which reads the data from the file sequentially.
Transforms CSV raw data into an event.
Creates a batch of event data.
Then pushes a batch into the Kinesis stream.

2. A `consumer`, which polls from the Kinesis stream.
Aggregates the event data.
And writes the result into persistent storage.


## Concurrent, Synchronization via Messages, Asynchronous

### Design with two modules

1. Separates reading the file from pushing the event data into Kinesis.
Assuming it is a blocking API into Kinesis.
Inside the module those two concerns run concurrently and synchronize via messages.

2. The `consumer` is separated into three concerns.
The event data is piped via messages from step to step.

* Execution is on a single compute node.
* Scaling is limited by the number of cores on the node.

### Design with five modules

1. Reads the file and forwards events via messages.

2. Receives messages and pushes them into Kinesis.
Again assuming a blocking Kinesis API.

3. Pulls events from Kinesis and forwards via messages.
Same assumption as in *2.*.

4. Receives messages and aggregates the data.
Sends results via messages.

5. Receives messages and writes events to persistent storage.
Again assuming a blocking API of the persistent storage.


## Thoughts on which Tech is a good fit

### Great-to-Have
* plug into an already existing stream
* many different programming lanuages are supported (Python, Java, Scala, ..)
* elastic scaling is supported


### Forces

#### Programming Model
* what does the code of a processing step look like?
* is it similar to Apache Sparck
* read from InputStream, process, write to OutputStream
* what operators are provided on the stream?
* the abstractions offered to the programmer

#### Scaling
* partitions or shards of the message queue (stream)
* many *consumers* per message queue (locks?)
* elastic
* load-balancing

#### Resilient, Fault-Tolerance
* persistent message queue
* supervisor processes
* idempotent actors
* rate limiting
* backlog, circuit-breaker

#### Message Queue
* non-blocking
* lock-free
* high-performance (e.g. Aeron)


### Available Libs, Frameworks

#### Akka
* limited to Scala, Java (C#)
* actors communicating via messages
* targets software engineers

#### Apache Spark
*

#### Qlib
* 

#### Vert.x
* build microservice-based applications

#### ReactiveX
* perform complex operations on multiple asynchronous streams of data.
* 
