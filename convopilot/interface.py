from abc import ABC, abstractmethod

class PipelineModule:
    def __init__(self):
        self.input_queue = None
        self.output_queues = []

    def set_input_queue(self, q):
        self.input_queue = q

    def add_output_queue(self, q):
        self.output_queues.append(q)

    def output_data(self, data):
        for queue in self.output_queues:
            queue.put(data)


class AudioRecorder(ABC, PipelineModule):
    @abstractmethod
    def record(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class AudioTranscriber(ABC, PipelineModule):
    @abstractmethod
    def transcribe(self):
        pass

class InsightGenerator(ABC, PipelineModule):
    @abstractmethod
    def generate(self):
        pass