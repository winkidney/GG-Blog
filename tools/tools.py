#coding:utf-8
#!/usr/bin/python
#tools for test and so on

import time
import functools

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        start = time.clock()
        result = func(*args,**kwargs)
        end = time.clock()
        print 'used:', end - start
        return result
    return wrapper

