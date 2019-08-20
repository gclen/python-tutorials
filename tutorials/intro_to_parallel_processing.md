## An introduction to parallel programming in Python

There are many cases where you will want to speed up your code by splitting up the work using multiple processes or threads. There are many libraries and ways of doing this in Python but it can be overwhelming to try and figure out which library and method is best for your particular problem. Additionally, parallel programming can result in some tricky and hard to diagnose bugs. The goal of this guide is to give you enough background to start parallelizing your code and know enough terminology to try and diagnose any issues that might come up.

### Can you parallelize your problem?

First you need to think about how your problem can be split up among multiple workers. The best case scenario is that you have an [embarrassingly parallel problem](https://en.wikipedia.org/wiki/Embarrassingly_parallel) where there are no dependencies between the different workers. This could include 

* Reading in a bunch of files from a directory, modifying them and outputting them to a different directory
* Multiple runs of an algorithm on the same dataset (e.g. Monte Carlo simulations)
* Making a large number of calls to a database or REST API

In these cases, there is minimal overhead between all of the workers and you should see near linear scaling. For example, if 1 worker completed the task in 60 seconds, 6 workers should be able to complete the same task in close to 10 seconds.

There are many problems which require shared state or dependencies between the workers. Due to the additional overhead of keeping track of these dependencies, you won't see the same scaling as you would with an embarrassingly parallel problem. For example, the task that took 1 worker 60 seconds may take 6 workers 20 seconds. While this is still an overall speedup and worth doing, you will need to check how the runtime changes as you increase the number of workers.  

### When should you use processes versus threads?

Once you have figured out how to paralleize your problem, the next question is whether you should use processes or threads. If your problem is CPU intensive (i.e. you are doing a lot of number crunching) then you should use processes. If your bottleneck is coming from IO operations (e.g. making a bunch of calls to a database) then you should use multiple threads. If you use threads for a CPU intensive problem, you will probably not see a huge speedup since all of the threads are sharing time on the CPU.  

### How do I actually do this in Python?

In my opinion, the best way to do this is with the [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) library. I like this library because it has a relatively simple interface and is included in the standard library.


### Using multiple threads via the ThreadPoolExecutor

One common use case is making multiple queries to an API. Since this is IO intensive, you will want to use a ThreadPool. From the concurrent.futures documentation:

```python
import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
```

In this case you have a list of URLs which you want to get the contents from. Let's break down the individual steps

1) Define your function which will do the actual work. In this case it is the ```load_url``` function which takes in a URL and fetches the content at that URL.
2) Create the ThreadPoolExecutor with a specified number of workers
3) Submit your tasks to the executor. In this case it is passing the list of URLs (along with the timeout parameter) to the ```load_url``` function. This returns a bunch of [Future](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) objects. You can query these Future objects to see if they are still running, if any exceptions were raised and get the results.
4) Loop over all of these Future objects and try to get the results once they have completed. If any exceptions were raised you can catch them so that you can continue your processing.

### Using multiple processes via the ProcessPoolExecutor

If your task is CPU intensive, you will want to use multiple processes. Python does this by spawning multiple interpreters (this is done to get around the [Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock)).

Here is an example of using processes to see if numbers in a list are prime (adapted from the Python3 documentation). Warning: if you do not specify max_workers then it will use all of the cores on your system.

```python
import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

    # Start the load operations and mark each future with its URL
    future_is_prime = {executor.submit(is_prime, number):number for number in PRIMES}
    for future in concurrent.futures.as_completed(future_is_prime):
        prime = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (prime, exc))
        else:
            if data:
                print('%d is a prime number' % (prime))
            else:
                print('%d is not a prime number' % (prime))

if __name__ == '__main__':
    main()

```

### How do I check that I am actually getting a performance boost?

You should time how long your task takes in serial (i.e. with 1 worker) and using multiple workers.

### Potential issues that you might run into

* Deadlocks: These occur when two or more workers depend on the result of each other. For example if thread A is waiting on thread B and vice-versa then you will have a deadlock.
* Race conditions: If two or more threads/processes are trying to update shared state at the same time then you might not get the results you expect. These can be very tricky to track down (since it might not happen every time) so be careful when using shared state!
* Unfortunately you cannot share memory between processes (since they are separate interpreters). However this has been fixed in [Python 3.8](https://docs.python.org/3.9/library/multiprocessing.shared_memory.html) but it requires the multiprocessing library.

### What other libraries can I use?

* Multiprocessing: This is also a part of the standard library and gives you access to low level controls such as locks and queues. It can be powerful but harder to use.
* Pebble: This is a third-party library that is a thin wrapper around concurrent.futures. It has some nice benefits (such as terminating processes after they exceed a time limit) but I would only use it if you find concurrent.futures does not meet your needs.