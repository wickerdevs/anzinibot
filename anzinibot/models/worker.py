from anzinibot import applogger
from threading import Thread
import queue
import time
from typing import List

class TaskQueue(queue.Queue):

    def __init__(self, num_workers=1, names:list=None):
        queue.Queue.__init__(self)
        self.num_workers = num_workers
        self.names = names
        self.workers:List[Thread] = list()
        self.stopping: bool = False
        self.start_workers()

    def add_task(self, task, *args, **kwargs):
        args = args or ()
        kwargs = kwargs or {}
        self.put((task, args, kwargs))

    def start_workers(self):
        for i in range(self.num_workers):
            if self.names and len(self.names) >= i+1:
                t = Thread(target=self.worker, name=self.names[i])
            else:
                t = Thread(target=self.worker)
            t.daemon = True
            t.start()
            self.workers.append(t)

    def worker(self):
        while True:
            if self.stopping:
                break
            item, args, kwargs = self.get()
            item(*args, **kwargs)  
            self.task_done()

    def close(self):
        self.stopping = True
        self.join()
        applogger.info(f'Closed queue')