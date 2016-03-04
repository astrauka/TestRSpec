import sys
from threading import Thread
try:
  from Queue import Queue, Empty
except ImportError:
  from queue import Queue, Empty  # python 3.x

class NonBlockingStreamReader:
  def __init__(self, stream):
    self.queue = Queue()

    def _populateQueue(stream, queue):
      for char in iter(lambda: stream.read(1), ''):
        queue.put(char)
      stream.close()

    thread = Thread(target=_populateQueue, args=(stream, self.queue))
    thread.daemon = True # thread dies with the program
    thread.start()

  def read(self):
    try:
      return self.queue.get_nowait() # or q.get(timeout=.1)
    except Empty:
      return None






# from threading import Thread
# try:
#   from Queue import Queue, Empty
# except ImportError:
#   from queue import Queue, Empty  # python 3.x

# class NonBlockingStreamReader:
#   def __init__(self, stream):
#     self._stream = stream
#     self._queue = Queue()

#     def _populateQueue(stream, queue):
#       for char in iter(lambda: stream.read(1), ''):
#         queue.put(char)

#     self._thread = Thread(target = _populateQueue, args = (self._stream, self._queue))
#     self._thread.daemon = True
#     self._thread.start() #start collecting lines from the stream

#   def read(self, timeout = None):
#     try:
#       return self._queue.get(block = timeout is not None, timeout = timeout)
#     except Empty:
#       return None
