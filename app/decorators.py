# -*- coding: utf-8 -*-
from threading import Thread
from multiprocessing import Process


def async(use_process=False):
    """
    异步调用,
    :param use_process: 是否使用进程,默认使用线程
    :return:
    """
    def async_wrapper(func):
        def wrapper(*args, **kwargs):
            if use_process:
                process = Process(target=func, args=args, kwargs=kwargs)
                process.start()
            else:
                thread = Thread(target=func, args=args, kwargs=kwargs)
                thread.start()
        return wrapper
    return async_wrapper
