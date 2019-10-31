import multiprocessing as mp
from multiprocessing import Value
import time

counter = Value('i', 0)


def task(taskvar):
    print('start: ' + taskvar)
    time.sleep(3)
    with counter.get_lock():
        counter.value += 1
        print('end: ' + taskvar + str(counter.value))


def main():
    tasks = ['a', 'b', 'c', 'd', 'e']

    pool = mp.Pool(2)
    for taskvar in tasks:
        pool.apply_async(task, args=(taskvar))

    print('all tasks sub')
    # Tell the pool that there are no more tasks to come and join
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
