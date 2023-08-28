
import queue
import threading


class Pipeline:
    def __init__(self, stop_func):
        self.modules = {}
        self.threads = []
        self.stop_func = stop_func

    def add_module(self, module, upstreams=[]):
        module_name = module.name
        if module_name in self.modules:
            raise ValueError(f"Module with name {module_name} already exists!")

        for upstream_name in upstreams:
            upstream = self.modules.get(upstream_name)
            if not upstream:
                raise ValueError(f"Dependency {upstream_name} not found!")

            q = queue.Queue()
            upstream.add_output_queue(q)
            module.set_input_queue(q)

        self.modules[module_name] = module

    def start(self, create_thread_func=threading.Thread):
        for module in self.modules.values():
            thread = create_thread_func(target=module.run)
            thread.start()
            self.threads.append(thread)

    def wait_until_complete(self):
        for thread in self.threads:
            thread.join()

    def stop(self):
        self.stop_func()
        self.wait_until_complete()