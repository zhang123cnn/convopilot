import pyaudio
from convopilot.interface import PipelineModule


class PyAudioRecorder(PipelineModule):
    def __init__(self, name, chunk_duration, rate, channels, chunk, format):
        super().__init__(name)
        self.chunk_duration = chunk_duration
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.format = format

    def onStart(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format, channels=self.channels, rate=self.rate,
                                  input=True, frames_per_buffer=self.chunk)

    def process(self, items):
        chunk_data = b''
        for _ in range(0, int(self.rate / self.chunk * self.chunk_duration)):
            if self.should_stop:
                break
            data_ = self.stream.read(self.chunk)
            chunk_data += data_

        self.output_data(chunk_data)

    def onFinish(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        print("Stopped recording.")
