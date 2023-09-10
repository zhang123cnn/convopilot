from abc import ABC, abstractmethod
import logging


class PipelineModule(ABC):
    def __init__(self, name):
        self.name = name
        self.input_queue = None
        self.output_queues = []
        self.should_stop = False

    def set_input_queue(self, q):
        self.input_queue = q

    def add_output_queue(self, q):
        self.output_queues.append(q)

    def output_data(self, data):
        for queue in self.output_queues:
            queue.put((data, self.name))

    def run(self):
        while not self.should_stop:
            if (self.input_queue is None):
                self.process_with_logging(None, None)
                continue

            data, source = self.input_queue.get()
            if data is None:
                break

            self.process_with_logging(data, source)

        self.output_data(None)
        self.onFinish()

    def process_with_logging(self, data, source):
        logging.debug(f'{self.name} - start processing once')
        self.process(data, source)
        logging.debug(f'{self.name} - end processing once')

    def stop(self):
        self.should_stop = True

    @abstractmethod
    def process(self, data, source):
        pass

    @abstractmethod
    def onFinish(self):
        pass