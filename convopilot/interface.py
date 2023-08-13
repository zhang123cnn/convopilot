from abc import ABC, abstractmethod

class AudioRecorder(ABC):
    @abstractmethod
    def record(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class AudioTranscriber(ABC):
    @abstractmethod
    def transcribe(self):
        pass

class InsightGenerator(ABC):
    @abstractmethod
    def generate(self):
        pass