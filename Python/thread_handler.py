import threading

class FMSThread(threading.Thread):
    def __init__(self, target, args=(), kwargs=None):
        super().__init__(target=target, args=args, kwargs=kwargs or {}, daemon=True)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()


class ThreadHandler:
    """
    Class to handle the creation, variable interfacing, and destruction of threads.
    """
    def __init__(self):
        self.threads = {}

    def create_thread(self, name, target, *args, **kwargs):
        if name not in self.threads:
            thread = FMSThread(target=target, args=args, kwargs=kwargs)
            self.threads[name] = thread
            return thread
        else:
            raise Exception(f"Thread {name} already exists but was attempted to be created again.")

        
    def start_thread(self, name):
        if name in self.threads:
            if not self.threads[name].is_alive():
                self.threads[name].start()
            else:
                raise Exception(f"Thread {name} is already running.")
        else:
            raise Exception(f"Thread {name} does not exist but was attempted to be started.")
        
    def start_all_threads(self):
        for name in self.threads:
            if not self.threads[name].is_alive():
                self.threads[name].start()
            else:
                raise Exception(f"Thread {name} is already running.")
            
    def is_thread_running(self, name):
        if name in self.threads:
            return self.threads[name].is_alive()
        else:
            raise Exception(f"Thread {name} does not exist but was attempted to be checked.")
        
    def get_thread(self, name):
        if name in self.threads:
            return self.threads[name]
        else:
            raise Exception(f"Thread {name} does not exist but was attempted to be accessed.")
        
    def stop_thread(self, name):
        if name in self.threads:
            if self.threads[name].is_alive():
                self.threads[name].stop()
            del self.threads[name]
        else:
            raise Exception(f"Thread {name} does not exist but was attempted to be stopped.")
        
    def stop_all_threads(self):
        for name in list(self.threads.keys()):
            self.stop_thread(name)