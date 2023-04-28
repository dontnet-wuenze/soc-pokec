# SuperFastPython.com
# example of sharing a lock with worker processes using a global variable
from random import random
from time import sleep
from multiprocessing import set_start_method
from multiprocessing import Lock
from multiprocessing.pool import Pool


# task executed in a worker process
def task(identifier):
    # acquire the mutex lock
    with lock:
        # generate a value
        value = random()
        # block for a moment
        sleep(value)
        # report a message
        print(f'Task {identifier} completed with {value}', flush=True)


# protect the entry point
if __name__ == '__main__':
    # set the fork start method
    set_start_method('fork')
    # create the shared lock instance
    lock = Lock()
    # create and configure the process pool
    with Pool(4) as pool:
        # issue tasks into the process pool
        result = pool.map_async(task, range(10))
        # wait for all tasks to finish
        result.wait()