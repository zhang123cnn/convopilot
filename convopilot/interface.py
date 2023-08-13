from abc import ABC, abstractmethod

class AudioRecorder(ABC):
    @abstractmethod
    def record(self, output_queue):
        pass

    @abstractmethod
    def stop(self):
        pass

class AudioTranscriber(ABC):
    @abstractmethod
    def transcribe(self, input_queue, output_queue):
        pass

class InsightGenerator(ABC):
    @abstractmethod
    def generate(self, input_queue):
        pass