import multiprocessing as mp
import inject
import Queue as StdQueue
import time

import producer
import consumer


# Injector
#
def pipeline(binder):
  binder.install(producer.file_base)
  binder.install(consumer.queue_base)

  q = mp.Queue()
  binder.bind(mp.Queue, q)

  write_func = producer.queue_create_write(q)
  binder.bind(producer.EventWriter, producer.DefaultEventWriter(write_func))
  binder.bind(consumer.Stream, consumer.infinite_mpqueue_stream(q))


inject.configure(pipeline)


# Stream Processing
#
def worker(q):
  consumer.consume()


q = inject.instance(mp.Queue)

p = mp.Process(target=worker, args=(q,))
p.start()

producer.produce()

q.close()
q.join_thread()

p.join()
