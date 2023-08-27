
import queue
import threading


class Pipeline:
    def __init__(self):
        self.modules = {}
        self.threads = []

    def add_module(self, module_name, module, upstreams=[]):
        if module_name in self.modules:
            raise ValueError(f"Module with name {module_name} already exists!")

        for upstream in upstreams:
            q = queue.Queue()
            upstream.add_output_queue(q)
            module.set_input_queue(q)

        self.modules[module_name] = module

    def start(self):
        for module in self.modules.values():
            thread = threading.Thread(target=module.run)
            thread.start()
            self.threads.append(thread)

    def wait_until_complete(self):
        for thread in self.threads:
            thread.join()
