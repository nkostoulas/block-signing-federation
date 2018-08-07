#!/usr/bin/env python
import threading
import multiprocessing
from abc import ABC, abstractmethod

class Daemon(ABC):
    def __init__(self, event):
        self.stop_event = event
        self.daemon = True

    def stop(self):
        self.stop_event.set()

    @abstractmethod
    def run(self):
        pass

class DaemonThread(threading.Thread, Daemon):
    def __init__(self):
        threading.Thread.__init__(self)
        Daemon.__init__(self, threading.Event())

class DaemonProcess(multiprocessing.Process, Daemon):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        Daemon.__init__(self, multiprocessing.Event())
